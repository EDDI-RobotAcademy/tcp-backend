from django.db import models
from account.entity.account import Account


from account.entity.profile_gender_type import ProfileGenderType


class Profile(models.Model):
    nickname = models.CharField(max_length=64, unique=True)
    email = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64, default=None, null=True)  # 일반 회원가입일 경우 사용하는 비밀번호
    salt = models.CharField(max_length=16, default=None, null=True)
    gender = models.ForeignKey(ProfileGenderType, on_delete=models.CASCADE)   # 성별 필드 추가
    birthyear = models.IntegerField()           # 생년월일 필드 추가
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # 최초 등록일자 필드 추가
    last_login = models.DateTimeField(auto_now=True)      # 최근 접속시간 필드 추가

    def save(self, *args, **kwargs):
        if 'force_last_login' in kwargs:
            self._meta.get_field('last_login').auto_now = False
            self.last_login = kwargs.pop('force_last_login')
        super().save(*args, **kwargs)
        if 'force_last_login' not in kwargs:
            self._meta.get_field('last_login').auto_now = True

    def __str__(self):
        return f"Profile -> email: {self.email}, nickname: {self.nickname}"

    class Meta:
        db_table = 'profile'
        app_label = 'account'
