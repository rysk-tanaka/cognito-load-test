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
