# Cognito Load Test

AWS Cognitoの`initiate_auth`に対する負荷テストツール。
モックと実環境の両方でテストが可能です。

## 開発環境のセットアップ

### 前提条件

- Python 3.8以上
- uv

### セットアップ手順

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

## インストール

プロジェクトを使用するだけの場合：

```bash
uv pip install .
```

## 使用方法

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
```

## 設定オプション

`CognitoLoadTest`クラスは以下のパラメータを受け付けます：

- `total_requests`: 実行する総リクエスト数（デフォルト: 120）
- `duration_seconds`: 目標実行時間（秒）（デフォルト: 1）
- `config`: テスト設定（LoadTestConfig オブジェクト）

### 環境変数による設定

- `COGNITO_LOAD_TEST_USE_MOCK`: モックの使用有無（true/false）
- `AWS_REGION`: AWS リージョン
- `COGNITO_USER_POOL_ID`: 実環境テスト用のユーザープールID
- `COGNITO_CLIENT_ID`: 実環境テスト用のクライアントID

## プロジェクト構造

```
cognito-load-test/
├── pyproject.toml        # プロジェクト設定とビルド設定
├── README.md            # このファイル
├── cognito_load_test/   # ソースコード
│   ├── __init__.py
│   ├── load_test.py    # メインの負荷テストロジック
│   ├── config.py       # 設定管理
│   └── utils.py        # ユーティリティ関数
└── tests/               # テストコード
    ├── __init__.py
    └── test_load_test.py
```
