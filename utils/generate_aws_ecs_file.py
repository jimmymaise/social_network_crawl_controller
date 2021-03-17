import os
import json


def genertate_file():
    task_definition_template = {
        "family": os.getenv("FAMILY_NAME", "default-famility"),
        "taskRoleArn": os.getenv("TASK_ROLE_ARN", "arn:aws:iam::450253548902:role/ecsTaskExecutionRole"),
        "executionRoleArn": os.getenv("TASK_ROLE_ARN", "arn:aws:iam::450253548902:role/ecsTaskExecutionRole"),
        "networkMode": "awsvpc",
        "containerDefinitions": [
            {
                "name": os.getenv("CONTAINER_NAME", "aws-ecs-container"),
                "image": os.getenv("REPOSITORY_URL"),
                "environment": [
                    {
                        "name": "SERVICE_CONFIG",
                        "value": os.getenv("SERVICE_CONFIG"),
                    },
                    {
                        "name": "LAMBDA_X_API_KEY",
                        "value": os.getenv("LAMBDA_X_API_KEY"),
                    },
                    {
                        "name": "LAMBDA_BASE_URL",
                        "value": os.getenv("LAMBDA_BASE_URL"),
                    }
                ],
                "environmentFiles": [
                    {
                        "value": os.getenv("AWS_S3_ENV_OBJECT", "arn:aws:s3:::hiip-asia-env/ig.env"),
                        "type": "s3"
                    }
                ],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": os.getenv("LOG_GROUP_NAME", "default-log-group"),
                        "awslogs-region": "us-west-2",
                        "awslogs-stream-prefix": os.getenv("SERVICE_NAME", "ig-cluster"),
                    }
                }
            }
        ],
        "requiresCompatibilities": [
            "FARGATE"
        ],
        "cpu": os.getenv("DEFAULT_CPU", "256"),
        "memory": os.getenv("DEFAULT_CPU", "512")
    }
    with open("task_definition_file.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(task_definition_template))
    print('Create Task defintion + Service file is Done')


if __name__ == '__main__':
    genertate_file()
