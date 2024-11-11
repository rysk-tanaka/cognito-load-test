# Cognito Load Test

AWS Cognitoの`initiate_auth`に対する負荷テストツール。
モックと実環境の両方でテストが可能です。

## 目次

- [インストール](#インストール)
- [CLIの使用方法](#cli-の使用方法)
- [Python APIの使用方法](#python-apiの使用方法)
- [設定オプション](#設定オプション)
- [開発者向け情報](#開発者向け情報)

## インストール

### 前提条件

- Python 3.8以上
- uv
- AWS認証情報（実環境テスト時のみ必要）

### インストール手順

```bash
uv pip install .
```

## CLI の使用方法

インストール後、`cognito-load-test`コマンドが使用可能になります：

### 基本的な使用方法

```bash
# モック環境でのテスト
cognito-load-test --total-requests 100

# 実環境でのテスト
export COGNITO_USER_POOL_ID=your-pool-id
export COGNITO_CLIENT_ID=your-client-id
export COGNITO_USERNAME=testuser
export COGNITO_PASSWORD=testpass

cognito-load-test --use-mock false --auth-flow USER_SRP_AUTH --total-requests 50

# JSON形式での出力
cognito-load-test --output-format json
```

### 実行結果例

```json
{
  "total_requests": 120,
  "successful_requests": 120,
  "failed_requests": 0,
  "duration": 1.23,
  "requests_per_second": 97.56,
  "used_mock": true,
  "retry_mode": "standard",
  "username": "NwleiCQHsX"
}
```

### オプション

```
--total-requests    実行する総リクエスト数（デフォルト: 120）
--duration-seconds  目標実行時間（秒）（デフォルト: 1）
--use-mock         モック環境の使用（true/false、デフォルト: true）
--auth-flow        認証フロー（USER_PASSWORD_AUTH/USER_SRP_AUTH）
--retry-mode       Boto3のリトライモード（standard/adaptive、デフォルト: standard）
--output-format    出力形式（json/text、デフォルト: text）
```

### 環境変数による設定

設定は以下の環境変数で行います：

```bash
# 必須（実環境テスト時）
export COGNITO_USER_POOL_ID=your-pool-id
export COGNITO_CLIENT_ID=your-client-id

# オプション
export COGNITO_USERNAME=your-username      # 指定しない場合はランダム生成
export COGNITO_PASSWORD=your-password      # 指定しない場合はランダム生成
export COGNITO_LOAD_TEST_USE_MOCK=false   # デフォルト: true
export COGNITO_AUTH_FLOW=USER_SRP_AUTH    # デフォルト: USER_PASSWORD_AUTH
export COGNITO_RETRY_MODE=standard        # デフォルト: standard
export AWS_REGION=us-east-1               # デフォルト: us-east-1
```

## Python APIの使用方法

### モックを使用したテスト

```python
from cognito_load_test.load_test import CognitoLoadTest
from cognito_load_test.config import LoadTestConfig

# モックを使用した負荷テスト
config = LoadTestConfig(use_mock=True)
load_test = CognitoLoadTest(total_requests=120, duration_seconds=1, config=config)
results = load_test.run_test()

# 結果の表示
print(f"Total Requests: {results['total_requests']}")
print(f"Successful Requests: {results['successful_requests']}")
print(f"Failed Requests: {results['failed_requests']}")
print(f"Duration: {results['duration']:.2f} seconds")
print(f"Requests per Second: {results['requests_per_second']:.2f}")
```

### 実環境でのテスト

実環境でテストを行う場合は、以下の環境変数を設定する必要があります：

```bash
export COGNITO_USER_POOL_ID=your-user-pool-id
export COGNITO_CLIENT_ID=your-client-id
export AWS_REGION=us-east-1  # オプション（デフォルト: us-east-1）
export COGNITO_LOAD_TEST_USE_MOCK=false
```

```python
from cognito_load_test.load_test import CognitoLoadTest
from cognito_load_test.config import LoadTestConfig

# 実環境での負荷テスト
config = LoadTestConfig(use_mock=False)
load_test = CognitoLoadTest(total_requests=120, duration_seconds=1, config=config)
results = load_test.run_test()

# USER_SRP_AUTH を使用した実環境テスト
config = LoadTestConfig(use_mock=False, auth_flow="USER_SRP_AUTH")
load_test = CognitoLoadTest(config=config)
results = load_test.run_test()

# 特定のユーザーで認証テスト
config = LoadTestConfig(use_mock=False, auth_flow="USER_SRP_AUTH", username="hoge", password="fuga")
load_test = CognitoLoadTest(config=config)
results = load_test.run_test()
```

## 設定オプション

`CognitoLoadTest`クラスは以下のパラメータを受け付けます：

- `total_requests`: 実行する総リクエスト数（デフォルト: 120）
- `duration_seconds`: 目標実行時間（秒）（デフォルト: 1）
- `config`: テスト設定（LoadTestConfig オブジェクト）

`LoadTestConfig`クラスは以下のパラメータを受け付けます：

- `use_mock`: モックの使用有無（デフォルト: True）
- `aws_region`: AWSリージョン（デフォルト: "us-east-1"）
- `auth_flow`: 認証フロー（"USER_PASSWORD_AUTH" または "USER_SRP_AUTH"）（デフォルト: "USER_PASSWORD_AUTH"）
- `username`: 認証に使用するユーザー名（デフォルト: None、指定がない場合はランダム生成）
- `password`: 認証に使用するパスワード（デフォルト: None、指定がない場合はランダム生成）

### 環境変数による設定

- `COGNITO_LOAD_TEST_USE_MOCK`: モックの使用有無（true/false）
- `AWS_REGION`: AWS リージョン
- `COGNITO_AUTH_FLOW`: 認証フロー（USER_PASSWORD_AUTH または USER_SRP_AUTH）
- `COGNITO_USER_POOL_ID`: 実環境テスト用のユーザープールID
- `COGNITO_CLIENT_ID`: 実環境テスト用のクライアントID
- `COGNITO_USERNAME`: 認証に使用するユーザー名
- `COGNITO_PASSWORD`: 認証に使用するパスワード

## 開発者向け情報

### 開発環境のセットアップ

1. リポジトリのクローン：
```bash
git clone https://github.com/rysk-tanaka/cognito-load-test.git
cd cognito-load-test
```

2. 仮想環境の作成と有効化：
```bash
uv venv
# Unixの場合
source .venv/bin/activate
# Windowsの場合
# .venv\Scripts\activate
```

3. 開発用依存関係のインストール：
```bash
uv pip install -e ".[dev]"
```

### 開発用コマンド

- テストの実行：
```bash
pytest
```

- コードフォーマット：
```bash
ruff format .
```

- リンター実行：
```bash
ruff check .
```

## プロジェクト構造

```
cognito-load-test/
├── pyproject.toml        # プロジェクト設定とビルド設定
├── README.md            # このファイル
├── cognito_load_test/   # ソースコード
│   ├── __init__.py
│   ├── load_test.py    # メインの負荷テストロジック
│   ├── config.py       # 設定管理
│   ├── cli.py          # CLIインターフェース
│   └── utils.py        # ユーティリティ関数
└── tests/               # テストコード
    ├── __init__.py
    └── test_load_test.py
```

### 注意事項

- モックテスト時は自動的に `USER_PASSWORD_AUTH` が使用されます
- `USER_SRP_AUTH` は実環境テスト時のみ有効です
- 1回のテスト実行内では、同じ認証情報が再利用されます
  - 設定ファイルまたは環境変数で指定された認証情報を使用
  - 指定がない場合は、初回実行時にランダム生成された値を使用
- 実環境テストで特定のユーザーを使用する場合、そのユーザーが Cognito ユーザープールに存在している必要があります
