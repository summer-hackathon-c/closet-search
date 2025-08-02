from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


# Create your models here.
# カスタムユーザーモデルの使用に伴う、ユーザー作成方法を定義
class user_manager(BaseUserManager):
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
class users(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    admin_flag = models.BooleanField(default=False)
    # passwordは記載不要。AbstractBaseUserに含まれているため

    objects = user_manager()

    # 一意の識別子として使用される(ログイン時)
    USERNAME_FIELD = "email"
    # superuser作成時追加で求められるフィールド
    REQUIRED_FIELDS = ["user_name"]

    def __str__(self):
        return self.user_name


# itemsテーブル
class items(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    create_date = models.DateField(auto_now_add=True)  # 編集したら変更となる気がする
    purchase_date = models.DateField()
    price = models.IntegerField()
    season = models.PositiveBigIntegerField()
    description = models.CharField(max_length=50, null=True, blank=True)
    delete_flag = models.BooleanField(default=False)  # default:削除されていない
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)

    # データベースを管理する画面で、上記名前を表示させるように設定
    def __str__(self):
        return self.item_id

    # 以下の名前を基準として並び替を行う
    class Meta:
        ordering = ["purchse_date"]


# tagsテーブル
class tags(models.Model):
    tag_id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(max_length=50)
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)

    # データベースを管理する画面で、上記名前を表示させるように設定
    def __str__(self):
        return self.tag_name

    # 以下の名前を基準として並び替を行う
    class Meta:
        ordering = ["tag_id"]


# item_tagsテーブル(中間テーブル)
class item_tags(models.Model):
    item_id = models.ForeignKey(items)
    tag_id = models.ForeignKey(tags, on_delete=models.CASCADE)


# items_photosテーブル
class item_photos(models.Model):
    photo_id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=255)

    # データベースを管理する画面で、上記名前を表示させるように設定
    def __str__(self):
        return self.photo_id

    # 以下の名前を基準として並び替を行う
    class Meta:
        ordering = ["photo_id"]


# #wearing_historiesテーブル
# class wearing_histories(models.Model):
#     wearing_history_id = models.BigAutoField(primary_key=True)
#     wearing_date = models.DateField()
#     description = models.CharField(max_length=100, null=True, blank=True)

#     #データベースを管理する画面で、上記名前を表示させるように設定
#     def __str__(self):
#         return self.wearing_history_id

#     #以下の名前を基準として並び替を行う
#     class Meta:
#         ordering = ["wearing_history_id"]


# #wearing_itemsテーブル（中間テーブル）
# class wearing_items(models.Model):
#     wearing_history_id = models.ForeignKey(wearing_histories, on_delete=models.CASCADE)
#     item_id = models.ForeignKey(items)
