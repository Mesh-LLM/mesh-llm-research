
import asyncio, json, sys
import aiohttp
import swerex.runtime.remote as remote
from swerex.runtime.abstract import ReadFileRequest

async def main():
    client = remote.RemoteRuntime(auth_token="fixture", host=sys.argv[1], timeout=0.5)
    result = {"module": remote.__file__}
    try:
        response = await asyncio.wait_for(client.read_file(ReadFileRequest(path="fixture")), 5)
        result.update(content=response.content)
    except (TimeoutError, aiohttp.ClientError) as error:
        result.update(exception=type(error).__module__ + "." + type(error).__name__,
                      message=str(error), status=getattr(error, "status", None))
    print("SDK_RESULT=" + json.dumps(result))

asyncio.run(main())
