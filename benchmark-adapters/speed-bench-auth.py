from __future__ import annotations
import os
import runpy
import sys
import hashlib
import json
import threading
from urllib.parse import urlparse

import requests

# SDK data access is fixed to the admitted immutable local Parquet artifact.
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"
import pathlib
import datasets

speed_data = pathlib.Path(os.environ["SKIPPY_BENCH_SPEED_DATASET"])
if not speed_data.is_absolute() or speed_data.stat().st_size != 364138:
    raise ValueError("SPEED dataset path or size mismatch")
if hashlib.sha256(speed_data.read_bytes()).hexdigest() != "4f76bc45bdffb38712a5c26d7a7c9a9a791484b392a7b64a6ffb9abe48e02e26":
    raise ValueError("SPEED dataset digest mismatch")
speed_cache = pathlib.Path(os.environ["SKIPPY_BENCH_SPEED_DATASET_CACHE"])
if not speed_cache.is_absolute():
    raise ValueError("SPEED dataset cache must be absolute")
original_load_dataset = datasets.load_dataset

def pinned_configs(path, **kwargs):
    if path != "nvidia/SPEED-Bench" or kwargs:
        raise ValueError("unexpected SPEED dataset configuration lookup")
    return ["qualitative", "throughput_16k", "throughput_1k", "throughput_2k", "throughput_32k", "throughput_8k"]

def pinned_dataset(path, name=None, split=None, **kwargs):
    if path != "nvidia/SPEED-Bench" or name != "qualitative" or split != "test" or kwargs:
        raise ValueError("unexpected SPEED dataset request")
    return original_load_dataset("parquet", data_files={"test": str(speed_data)}, split="test", cache_dir=str(speed_cache))

datasets.get_dataset_config_names = pinned_configs
datasets.load_dataset = pinned_dataset

original_request = requests.sessions.Session.request

def request_origin(url):
    if "://" not in url:
        url = "http://" + url
    parsed = urlparse(url)
    default_port = 443 if parsed.scheme.lower() == "https" else 80
    return (parsed.scheme.lower(), parsed.hostname, parsed.port or default_port)

benchmark_origin = request_origin(os.environ["SKIPPY_BENCH_BASE_URL"])

def authorized_request(self, method, url, **kwargs):
    if request_origin(url) == benchmark_origin:
        headers = dict(kwargs.get("headers", {}) or {})
        headers.setdefault("Authorization", f"Bearer {os.environ['SKIPPY_BENCH_API_KEY']}")
        kwargs["headers"] = headers
    return original_request(self, method, url, **kwargs)

requests.sessions.Session.request = authorized_request

timings_path = os.environ.get("SKIPPY_BENCH_RESPONSE_TIMINGS_PATH")
timings_lock = threading.Lock()
original_json = requests.models.Response.json

def sha256_json(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def request_sha256(response):
    try:
        body = response.request.body
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        payload = json.loads(body)
        user_messages = [
            {"role": message.get("role"), "content": message.get("content")}
            for message in payload.get("messages", [])
            if isinstance(message, dict) and message.get("role") == "user"
        ]
        return sha256_json({
            "messages": user_messages,
            "model": payload.get("model"),
            "max_tokens": payload.get("max_tokens"),
        })
    except Exception:
        return None

def response_sha256(response):
    try:
        choices = response.get("choices")
        choice = choices[0]
        message = choice.get("message")
        content = message.get("content") if isinstance(message, dict) else choice.get("text")
        return sha256_json({"content": content, "finish_reason": choice.get("finish_reason")})
    except Exception:
        return None

def capture_response_timings(self, *args, **kwargs):
    response = original_json(self, *args, **kwargs)
    timings = response.get("timings") if isinstance(response, dict) else None
    if (
        timings_path
        and isinstance(timings, dict)
        and not getattr(self, "_skippy_timings_captured", False)
    ):
        # Preserve only scalar timing counters and one-way hashes; never copy content.
        safe_timings = {
            key: value
            for key, value in timings.items()
            if isinstance(key, str) and isinstance(value, (bool, int, float))
        }
        record = {
            "request_sha256": request_sha256(self),
            "response_sha256": response_sha256(response),
            "timings": safe_timings,
        }
        with timings_lock:
            with open(timings_path, "a", encoding="utf-8") as output:
                output.write(json.dumps(record, sort_keys=True) + "\n")
        self._skippy_timings_captured = True
    return response

requests.models.Response.json = capture_response_timings
script = sys.argv.pop(1)
sys.argv[0] = script
runpy.run_path(script, run_name="__main__")
