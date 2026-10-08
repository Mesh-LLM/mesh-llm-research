import sys

import yaml
from sweagent.agent.problem_statement import TextProblemStatement
from sweagent.environment.repo import PreExistingRepoConfig
from sweagent.environment.swe_env import EnvironmentConfig
from sweagent.run.batch_instances import BatchInstance
from swerex.deployment.config import DockerDeploymentConfig

source, target, platform = sys.argv[1:4]
with open(source) as handle:
    simple_instances = yaml.safe_load(handle)

docker_args = [
    "--entrypoint",
    "",
]
instances = []
for item in simple_instances:
    deployment = DockerDeploymentConfig(
        image=item["image_name"],
        docker_args=docker_args,
        platform=platform or None,
        python_standalone_dir="/root",
        startup_timeout=1800,
    )
    instance = BatchInstance(
        env=EnvironmentConfig(
            deployment=deployment,
            repo=PreExistingRepoConfig(
                repo_name=item.get("repo_name") or "app",
                base_commit=item.get("base_commit") or "HEAD",
            ),
        ),
        problem_statement=TextProblemStatement(
            text=item["problem_statement"],
            id=item["instance_id"],
            extra_fields=item.get("extra_fields") or {},
        ),
    )
    instances.append(instance.model_dump(mode="json", exclude_none=True))

with open(target, "w") as handle:
    yaml.safe_dump(instances, handle, sort_keys=False)
