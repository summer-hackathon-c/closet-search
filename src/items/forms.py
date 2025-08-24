from django import forms
from .models import User, Item, ItemPhoto
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
    # createでも同じUIを使えるように追加
    # 画像をアップロードするためのフォーム（Itemモデルにフィールドなくても問題なし）
    images = forms.FileField(
        label="写真は5枚まで登録できます",
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": True,  # 複数画像選択可能
                "accept": "image/*",  # 画像ファイルのみ選択可能
                "id": "images-input",  # HTMLのiD属性
            }
        ),
        required=False,  # view側にて設定
    )

    class Meta:
        model = Item
        fields = ["purchase_date", "price", "description"]
        labels = {
            "purchase_date": "購入日",
            "price": "価格",
            "description": "説明・メモ",
        }

        # 入力欄のカスタマイズ
        widgets = {
            "purchase_date": forms.DateInput(
                attrs={
                    "class": "form-control",  # CSSにて使用するクラス
                    "type": "date",  # カレンダー形式の選択
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",  # CSSにて使用するクラス
                    "placeholder": "2000",
                    "min": "0",  # マイナスの価格入力がブラウザ上で禁止される
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",  # CSSにて使用するクラス
                    "rows": 4,  # 初期表示で4行文の高さに設定
                    "placeholder": "例：〇〇(店名,場所）にて購入",
                }
            ),
        }


# アイテム編集フォーム
class ItemUpdateForm(forms.ModelForm):
    # 画像をアップロードするためのフォーム（Itemモデルにフィールドなくても問題なし）
    images = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": True,  # 複数画像選択可能
                "accept": "image/*",  # 画像ファイルのみ選択可能
                "id": "images-input",  # HTMLのiD属性
            }
        ),
        required=False,  # view側にて設定
    )

    # 編集対象のアイテムのdescriptionが空欄であれば、空文字にする。
    def __init__(self, *args, **kwargs):
        # UpdateViewから渡すrequestを保持
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.description is None:
            self.fields["description"].initial = ""

        # Itemモデルの中に写真フィールドがないため、以下定義が必要
        self.fields["images"].label = "写真は5枚まで登録できます"

    # itemモデルの中から、指定フィールドを選択しラベルを表示
    class Meta:
        model = Item
        fields = ["purchase_date", "price", "description", "images"]
        labels = {
            "purchase_date": "購入日",
            "price": "価格",
            "description": "説明・メモ",
        }

        # 入力欄のカスタマイズ
        #  Updateのため、未入力が有り得るdescriptionのみplaceholder表示
        widgets = {
            "purchase_date": forms.DateInput(
                attrs={
                    "class": "form-control",  # CSSにて使用するクラス
                    # "placeholder": "2025-01-01",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",  # CSSにて使用するクラス
                    # "placeholder": "2000",
                    "min": "0",  # マイナスの価格入力がブラウザ上で禁止される
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",  # CSSにて使用するクラス
                    "rows": 4,  # 初期表示で4行文の高さに設定
                    "placeholder": "例：二子玉川で購入。かわいい！！",
                }
            ),
        }

    def clean(self):
        cleaned = super().clean()

        # 新規アップロード枚数
        files = []
        if hasattr(self, "files") and self.files:
            files = self.files.getlist("images")
        new_count = len(files)

        # 削除予定（×を押した既存画像）
        delete_ids = []
        if self.request and self.request.method == "POST":
            delete_ids = self.request.POST.getlist("delete_photos")

        # 既存の残る枚数（= 既存 - 削除）
        remaining = 0
        if self.instance and self.instance.pk:
            remaining = (
                ItemPhoto.objects.filter(item=self.instance)
                .exclude(id__in=delete_ids)
                .count()
            )

        total = remaining + new_count

        if total < 1:
            self.add_error("images", "写真は最低１枚登録してください")
        elif total > 5:
            self.add_error("images", "写真は最大５枚まで登録できます")

        return cleaned


# 季節タグの作成フォーム
class SeasonsSelectForm(forms.Form):
    # ビット演算にて定数の定義
    SEASON_SPRING = 1  # 0001
    SEASON_SUMMER = 2  # 0010
    SEASON_AUTUMN = 4  # 0100
    SEASON_WINTER = 8  # 1000

    # テンプレートにて使用
    SEASON_FLAGS = [
        (SEASON_SPRING, "春"),
        (SEASON_SUMMER, "夏"),
        (SEASON_AUTUMN, "秋"),
        (SEASON_WINTER, "冬"),
    ]

    # チェックボックスの定義
    # BoolianFieldはチェックボックス、required=Falseにて未選択でもエラーにならない。
    spring = forms.BooleanField(label="春", required=False)
    summer = forms.BooleanField(label="夏", required=False)
    autumn = forms.BooleanField(label="秋", required=False)
    winter = forms.BooleanField(label="冬", required=False)

    # 最低１つは選択しなければ、エラーが出るように定義
    # 親クラスのclean関数を上書き。フォーム全体をまとめてチェックするための関数。
    def clean(self):
        cleaned_data = super().clean()  # バリデーション済のデータを取得
        selected = [
            cleaned_data.get("spring"),
            cleaned_data.get("summer"),
            cleaned_data.get("autumn"),
            cleaned_data.get("winter"),
        ]
        if not any(selected):
            raise forms.ValidationError("季節は最低一つ選択してください")
        return cleaned_data

    # ユーザーが選択した季節を一つの数値にまとめて返す定義
    # 最初にValue=0と定義することによって、何も選ばれていない状態を作る。
    # バリデーション後、フォームに追加された値を取り出す。
    def get_season_value(self):
        value = 0
        if self.cleaned_data.get("spring"):
            value |= self.SEASON_SPRING
        if self.cleaned_data.get("summer"):
            value |= self.SEASON_SUMMER
        if self.cleaned_data.get("autumn"):
            value |= self.SEASON_AUTUMN
        if self.cleaned_data.get("winter"):
            value |= self.SEASON_WINTER
        return value
