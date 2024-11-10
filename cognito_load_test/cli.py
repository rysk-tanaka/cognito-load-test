import argparse
import json

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
        "--region", default="us-east-1", help="AWS region (default: us-east-1)"
    )
    parser.add_argument(
        "--auth-flow",
        choices=["USER_PASSWORD_AUTH", "USER_SRP_AUTH"],
        default="USER_PASSWORD_AUTH",
        help="Authentication flow to use (default: USER_PASSWORD_AUTH)",
    )
    parser.add_argument("--username", help="Username for authentication (optional)")
    parser.add_argument("--password", help="Password for authentication (optional)")
    parser.add_argument(
        "--output-format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    config = LoadTestConfig(
        use_mock=args.use_mock,
        aws_region=args.region,
        auth_flow=args.auth_flow,
        username=args.username,
        password=args.password,
    )

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


if __name__ == "__main__":
    main()
