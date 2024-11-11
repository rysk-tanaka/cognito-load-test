import pytest

from cognito_load_test.config import LoadTestConfig
from cognito_load_test.load_test import CognitoLoadTest


def test_load_test():
    load_test = CognitoLoadTest(total_requests=10, duration_seconds=1)
    results = load_test.run_test()

    assert results["total_requests"] == 10
    assert results["successful_requests"] + results["failed_requests"] == 10
    assert "duration" in results
    assert "requests_per_second" in results


def test_load_test_performance():
    load_test = CognitoLoadTest(total_requests=120, duration_seconds=1)
    results = load_test.run_test()

    assert results["requests_per_second"] >= 100  # 最低100rps以上であることを確認


def test_load_test_with_mock():
    config = LoadTestConfig(use_mock=True)
    load_test = CognitoLoadTest(total_requests=10, duration_seconds=1, config=config)
    results = load_test.run_test()

    assert results["total_requests"] == 10
    assert results["successful_requests"] + results["failed_requests"] == 10
    assert results["used_mock"] is True


@pytest.mark.skipif(
    "os.getenv('COGNITO_USER_POOL_ID') is None or os.getenv('COGNITO_CLIENT_ID') is None",
    reason="Real AWS credentials not configured",
)
def test_load_test_without_mock():
    config = LoadTestConfig(use_mock=False)
    load_test = CognitoLoadTest(total_requests=5, duration_seconds=1, config=config)
    results = load_test.run_test()

    assert results["total_requests"] == 5
    assert results["successful_requests"] + results["failed_requests"] == 5
    assert results["used_mock"] is False


@pytest.mark.skipif(
    "os.getenv('COGNITO_USER_POOL_ID') is not None or os.getenv('COGNITO_CLIENT_ID') is not None",
    reason="Environment variables are set - test should run only without credentials",
)
def test_load_test_without_mock_raises_error():
    config = LoadTestConfig(use_mock=False)
    load_test = CognitoLoadTest(config=config)

    with pytest.raises(ValueError) as exc_info:
        load_test.run_test()

    assert "Real environment requires" in str(exc_info.value)
