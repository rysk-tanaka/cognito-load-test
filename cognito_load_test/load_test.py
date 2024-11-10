import time
from concurrent.futures import ThreadPoolExecutor

import boto3
from moto import mock_aws

from cognito_load_test.utils import create_user_pool_and_client, random_string


class CognitoLoadTest:
    def __init__(self, total_requests=120, duration_seconds=1):
        self.total_requests = total_requests
        self.duration_seconds = duration_seconds
        self.successful_requests = 0
        self.failed_requests = 0

    def perform_auth_request(self, client, user_pool_id, client_id):
        """認証リクエストを実行"""
        try:
            client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                ClientId=client_id,
                AuthParameters={
                    "USERNAME": random_string(10),
                    "PASSWORD": random_string(12),
                },
            )
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @mock_aws
    def run_test(self):
        """負荷テストの実行"""
        cognito_client = boto3.client("cognito-idp", region_name="us-east-1")
        user_pool_id, client_id = create_user_pool_and_client(cognito_client)

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
                if future.result():
                    self.successful_requests += 1
                else:
                    self.failed_requests += 1

        end_time = time.time()
        duration = end_time - start_time

        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "duration": duration,
            "requests_per_second": self.total_requests / duration,
        }
