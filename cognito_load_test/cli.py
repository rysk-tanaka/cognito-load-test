import argparse
import json
import logging
import os

from cognito_load_test.config import LoadTestConfig
from cognito_load_test.load_test import CognitoLoadTest


def parse_args():
    parser = argparse.ArgumentParser(description="Cognito Load Test CLI")

    # 必須パラメータ
    parser.add_argument(
        "--total-requests",
        type=int,
        default=120,
        help="Total number of requests to perform (default: 120)",
    )

    # オプションパラメータ
    parser.add_argument(
        "--duration-seconds",
        type=int,
        default=1,
        help="Target duration in seconds (default: 1)",
    )
    parser.add_argument(
        "--use-mock",
        type=lambda x: x.lower() == "true",
        default=True,
        help="Use mock environment (default: true)",
    )
    parser.add_argument(
        "--auth-flow",
        choices=["USER_PASSWORD_AUTH", "USER_SRP_AUTH"],
        default="USER_PASSWORD_AUTH",
        help="Authentication flow to use (default: USER_PASSWORD_AUTH)",
    )
    parser.add_argument(
        "--retry-mode",
        choices=["standard", "adaptive"],
        default="standard",
        help="Boto3 retry mode (default: standard)",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )

    return parser.parse_args()


def main():
    # ログ設定
    logging.basicConfig(
        level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    args = parse_args()

    # 環境変数から設定を読み込み、CLIオプションで上書き
    config = LoadTestConfig.from_env()
    config.use_mock = args.use_mock
    config.auth_flow = args.auth_flow
    config.retry_mode = args.retry_mode

    load_test = CognitoLoadTest(
        total_requests=args.total_requests,
        duration_seconds=args.duration_seconds,
        config=config,
    )

    results = load_test.run_test()

    if args.output_format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(f"Total Requests: {results['total_requests']}")
        print(f"Successful Requests: {results['successful_requests']}")
        print(f"Failed Requests: {results['failed_requests']}")
        print(f"Duration: {results['duration']:.2f} seconds")
        print(f"Requests per Second: {results['requests_per_second']:.2f}")
        print(f"Used Mock: {results['used_mock']}")
        print(f"Retry Mode: {results['retry_mode']}")
        print(f"Username: {results['username']}")


if __name__ == "__main__":
    main()
