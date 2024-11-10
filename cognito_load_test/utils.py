import random
import string


def random_string(length: int) -> str:
    """ランダムな文字列を生成する補助関数"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_valid_password(length=12):
    """Cognitoのパスワードポリシーに準拠したパスワードを生成"""
    # 各文字種から最低1文字を確保
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    number = random.choice(string.digits)
    special = random.choice("!@#$%^&*()_+-=[]{}|'")

    # 残りの長さをランダムに埋める
    remaining_length = length - 4  # 確定した4文字を引く
    remaining_chars = "".join(
        random.choices(
            string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|'",
            k=remaining_length,
        )
    )

    # すべての文字を結合してシャッフル
    all_chars = list(lowercase + uppercase + number + special + remaining_chars)
    random.shuffle(all_chars)

    return "".join(all_chars)


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


def create_test_user(cognito_client, user_pool_id, username, password):
    """テスト用ユーザーを作成"""
    try:
        cognito_client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            TemporaryPassword=password,
            MessageAction="SUPPRESS",
        )

        # パスワードを確定
        cognito_client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=True,
        )
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
