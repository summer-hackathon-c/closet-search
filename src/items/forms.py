from django import forms
from .models import User
from .models import Item


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


# アイテム新規登録
class ItemForm(forms.ModelForm):
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
