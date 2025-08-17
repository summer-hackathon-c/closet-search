from django import forms
from .models import User, Item
from django.contrib.auth import authenticate
from django.forms import ValidationError


# ユーザー新規登録
class CustomUserCreationForm(forms.ModelForm):
    # 入力フィールドへ入力したパスワードは非表示で表示
    password1 = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    # 以下のクラスでモデルとフィールドを追加
    class Meta:
        model = User
        fields = ("user_name", "email")

    # ユーザーネームとメールアドレスとプレースホルダーとして表示(ラベル表示を非表示)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].label = ""
        self.fields["user_name"].widget.attrs["placeholder"] = "user name"
        self.fields["email"].label = ""
        self.fields["email"].widget.attrs["placeholder"] = "email"

    # 2つのパスワードが一致しているかの確認
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")
        return cleaned_data

    # パスワードをハッシュ化して保存する
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

    # emailの重複確認
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています。")
        return email


# ユーザーログイン画面
class LoginForm(forms.Form):
    # 入力フォームの作成
    email = forms.EmailField(
        label="", widget=forms.EmailInput(attrs={"placeholder": "email"})
    )
    password = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    # フォームインスタンスの初期化処理（承認済ユーザー情報を保持できる）
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request  # requestを保持(必要であれば)
        self.user = None

    # ユーザー情報の検証
    def clean(self):
        # バリデーション済の入力データ
        # (ユーザーによって入力された値が定義されたルールに従ってチェックされ、問題がないと判断されたデータ)
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # ユーザーがログイン可能かの判定
        if email and password:
            user = authenticate(
                email=email, password=password
            )  # 入力されたユーザー情報が正しいかを確認
            if user is None:
                raise ValidationError(
                    "メールアドレスまたはパスワードが正しくありません。"
                )
            else:
                self.user = user  # 認証に成功したユーザー情報を保存
        return cleaned_data  # 認証済データを次の処理に渡す

    def get_user(self):
        return (
            self.user
        )  # views.pyにて使用するため、保存しておいたユーザー情報を取り出す


# アイテム新規登録
class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["purchase_date", "price", "description"]
        labels = {
            "purchase_date": "購入日",
            "price": "価格",
            "description": "説明",
        }


# 画像アップロード
class PhotoUploadForm(forms.Form):
    # 複数枚アップロード
    images = forms.FileField(
        label="画像ファイル（複数可）",
        widget=forms.ClearableFileInput(
            attrs={"multiple": True, "accept": "image/*", "id": "images-input"}
        ),
        required=False,
    )
