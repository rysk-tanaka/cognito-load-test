import time
import os
import logging
from concurrent.futures import ThreadPoolExecutor

import boto3
from moto import mock_aws
from warrant_lite import WarrantLite as AWSSRP

from cognito_load_test import utils
from cognito_load_test.config import LoadTestConfig

logger = logging.getLogger(__name__)


class CognitoLoadTest:
    def __init__(self, total_requests=120, duration_seconds=1, config=None):
        self.total_requests = total_requests
        self.duration_seconds = duration_seconds
        self.successful_requests = 0
        self.failed_requests = 0
        self.config = config or LoadTestConfig.from_env()
        # 認証情報を保持
        self._username = None
        self._password = None

    def _get_auth_credentials(self):
        """認証情報を取得。初回のみ生成し、以降は同じ値を使用"""
        if not self._username:
            self._username = self.config.username or utils.random_string(10)
            self._password = self.config.password or utils.generate_valid_password()
        return self._username, self._password

    def perform_auth_request(self, client, user_pool_id, client_id):
        """認証リクエストを実行"""
        username, password = self._get_auth_credentials()
        try:
            if self.config.use_mock or self.config.auth_flow == "USER_PASSWORD_AUTH":
                response = client.initiate_auth(
                    AuthFlow="USER_PASSWORD_AUTH",
                    ClientId=client_id,
                    AuthParameters={
                        "USERNAME": username,
                        "PASSWORD": password,
                    },
                )
            else:
                aws = AWSSRP(
                    username=username,
                    password=password,
                    pool_id=user_pool_id,
                    client_id=client_id,
                    client=client,
                )
                srp_a = aws.get_auth_params()["SRP_A"]
                pre_response = client.initiate_auth(
                    AuthFlow="USER_SRP_AUTH",
                    ClientId=client_id,
                    AuthParameters={
                        "USERNAME": username,
                        "SRP_A": srp_a,
                    },
                )
                if "ResponseMetadata" in pre_response:
                    if pre_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        return True
                logger.error(f"Unexpected response format: {pre_response}")
                return False

                # TODO ここから先は未実装
                # if "ChallengeName" not in pre_response:
                #    return False
                # if pre_response["ChallengeName"] != "PASSWORD_VERIFIER":
                #    return False
                # if "ChallengeParameters" not in pre_response:
                #    return False
                # challenge_response = aws.process_challenge(
                #    pre_response["ChallengeParameters"]
                # )
                # response = client.respond_to_auth_challenge(
                #    ChallengeName="PASSWORD_VERIFIER",
                #    ClientId=client_id,
                #    ChallengeResponses=challenge_response,
                # )
            # レスポンスの検証
            if "AuthenticationResult" in response:
                return True
            logger.error(f"Unexpected response format: {response}")
            return False
        except Exception as e:
            logger.error(f"Error: {e}")
            return False

    @mock_aws
    def run_test_with_mock(self):
        """モックを使用したテストを実行"""
        return self._execute_test()

    def run_test_without_mock(self):
        """実環境に対してテストを実行"""
        if not all([os.getenv("COGNITO_USER_POOL_ID"), os.getenv("COGNITO_CLIENT_ID")]):
            raise ValueError(
                "Real environment requires COGNITO_USER_POOL_ID and COGNITO_CLIENT_ID"
            )
        return self._execute_test()

    def run_test(self):
        """設定に基づいてテストを実行"""
        if self.config.use_mock:
            return self.run_test_with_mock()
        else:
            return self.run_test_without_mock()

    def _execute_test(self):
        """テストの実際の実行ロジック"""
        cognito_client = boto3.client("cognito-idp", region_name=self.config.aws_region)

        # ユーザープールとクライアントIDの取得
        if self.config.use_mock:
            user_pool_id, client_id = utils.create_user_pool_and_client(cognito_client)
            # モックテスト用のユーザーを作成
            username, password = self._get_auth_credentials()
            utils.create_test_user(cognito_client, user_pool_id, username, password)
        else:
            user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
            client_id = os.getenv("COGNITO_CLIENT_ID")

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.total_requests) as executor:
            futures = []
            for _ in range(self.total_requests):
                futures.append(
                    executor.submit(
                        self.perform_auth_request,
                        cognito_client,
                        user_pool_id,
                        client_id,
                    )
                )

            for future in futures:
                try:
                    result = future.result(timeout=10)
                    if result:
                        self.successful_requests += 1
                    else:
                        self.failed_requests += 1
                except Exception as e:
                    logger.error(f"Future error: {str(e)}", exc_info=True)
                    self.failed_requests += 1

        end_time = time.time()
        duration = end_time - start_time

        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "duration": duration,
            "requests_per_second": self.total_requests / duration,
            "used_mock": self.config.use_mock,
            "username": self._username,
        }
