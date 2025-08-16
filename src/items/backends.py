from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# メールアドレスにてログインできるようにする、カスタム認証バックエンド
class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()  # CustomUserモデルを取得
        try:
            user = UserModel.objects.get(email=email)  # emailが一致するuser情報を取得
        except UserModel.DoesNotExist:
            return None

        # 入力されたパスワードがデータベースに保存されているハッシュ化されたパスワードと一致しているか確認。
        # ユーザーが有効か確認し、ログイン成功した場合
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None  # ログイン失敗
