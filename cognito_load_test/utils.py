import random
import string


def random_string(length: int) -> str:
    """ランダムな文字列を生成する補助関数"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def create_user_pool_and_client(cognito_client):
    """ユーザープールとクライアントを作成"""
    # ユーザープールの作成
    user_pool = cognito_client.create_user_pool(PoolName="TestPool")

    # クライアントの作成
    client = cognito_client.create_user_pool_client(
        UserPoolId=user_pool["UserPool"]["Id"],
        ClientName="TestClient",
        GenerateSecret=False,
    )

    return user_pool["UserPool"]["Id"], client["UserPoolClient"]["ClientId"]
