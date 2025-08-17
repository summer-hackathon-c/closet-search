from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


# Create your models here.
# カスタムユーザーモデルの使用に伴う、ユーザー作成方法を定義
class UserManager(BaseUserManager):
    # ユーザー登録
    def create_user(self, user_name, email, password=None):
        if not user_name:
            raise ValueError("Users must have an user_name")
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            user_name=user_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password):
        user = self.create_user(
            user_name=user_name,
            email=self.normalize_email(email),
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# usersテーブル（カスタムユーザーモデルを使用）
class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    admin_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # 自動セット、以降変更なし
    updated_at = models.DateTimeField(auto_now=True)  # 現在時刻にて自動更新される
    # passwordは記載不要。AbstractBaseUserに含まれているため

    objects = UserManager()

    # ログイン時一意の識別子として使用される
    USERNAME_FIELD = "email"
    # superuser作成時追加で求められるフィールド
    REQUIRED_FIELDS = ["user_name"]

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ["id"]  # 左記を基準にしてデータを並び替える
        db_table = "users"  # MySQLのテーブル名の指定


# itemsテーブル
class Item(models.Model):
    purchase_date = models.DateField()
    price = models.IntegerField()
    season = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=50, null=True, blank=True)
    delete_flag = models.BooleanField(default=False)  # default:削除されていない
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # データベースを管理する画面で、表示させる基準となるもの
    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["purchase_date"]  # 左記を基準にしてデータを並び替える
        db_table = "items"  # MySQLのテーブル名の指定


# tagsテーブル
class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # データベースを管理する画面で、以下を基準にして表示させる
    def __str__(self):
        return self.tag_name

    # 以下の名前を基準として並び替を行う
    class Meta:
        ordering = ["id"]  # 左記を基準にしてデータを並び替える
        db_table = "tags"  # MySQLのテーブル名の指定


# item_tagsテーブル(中間テーブル)
class ItemTag(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        ordering = ["item_id"]  # 左記を基準にしてデータを並び替える
        db_table = "item_tags"  # MySQLのテーブル名の指定


# item_photosテーブル
class ItemPhoto(models.Model):
    url = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    delete_flag = models.BooleanField(default=False)  # default:削除されていない
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # データベースを管理する画面で、以下を基準にして表示させる
    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["id"]  # 左記を基準にしてデータを並び替える
        db_table = "item_photos"  # MySQLのテーブル名の指定


# wearing_historiesテーブル
class WearingHistory(models.Model):
    wearing_date = models.DateField()
    description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # データベースを管理する画面で、以下を基準にして表示させる
    def __str__(self):
        return self.id

    class Meta:
        ordering = ["id"]  # 左記を基準にしてデータを並び替える
        db_table = "wearing_histories"  # MySQLのテーブル名の指定


# wearing_itemsテーブル（中間テーブル）
class WearingItem(models.Model):
    wearing_history = models.ForeignKey(WearingHistory, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)

    class Meta:
        ordering = ["wearing_history_id"]  # 左記を基準にしてデータを並び替える
        db_table = "wearing_items"  # MySQLのテーブル名の指定
