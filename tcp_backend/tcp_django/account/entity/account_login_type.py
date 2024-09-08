from django.db import models


class AccountLoginType(models.Model):
    class LoginType(models.TextChoices):
        KAKAO = 'KAKAO', 'Kakao'
        GENERAL = 'NORMAL', 'normal'
        GOOGLE = 'GOOGLE', 'google'

    loginType = models.CharField(max_length=10, choices=LoginType.choices, unique=True)

    def __str__(self):
        return self.loginType

    class Meta:
        db_table = 'account_login_type'
        app_label = 'account'