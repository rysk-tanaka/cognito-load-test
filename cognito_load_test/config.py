import os
from dataclasses import dataclass


@dataclass
class LoadTestConfig:
    use_mock: bool = True
    aws_region: str = "us-east-1"
    auth_flow: str = "USER_PASSWORD_AUTH"

    @classmethod
    def from_env(cls):
        """環境変数から設定を読み込む"""
        return cls(
            use_mock=os.getenv("COGNITO_LOAD_TEST_USE_MOCK", "true").lower() == "true",
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
            auth_flow=os.getenv("COGNITO_AUTH_FLOW", "USER_PASSWORD_AUTH"),
        )
