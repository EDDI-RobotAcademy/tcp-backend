from django.db import models

from account.entity.withdraw_reason import WithdrawReason
from account.entity.account_login_type import AccountLoginType
from account.entity.account_role_type import AccountRoleType


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    loginType = models.ForeignKey(AccountLoginType, on_delete=models.CASCADE)
    roleType = models.ForeignKey(AccountRoleType, on_delete=models.CASCADE)
    withdraw_reason = models.CharField(choices=WithdrawReason.choices, max_length=128, null=True)  # 탈퇴 사유
    withdraw_at = models.DateTimeField(null=True)   # 탈퇴 시점


    def __str__(self):
        return f"Account -> id: {self.id}, loginType: {self.loginType}, roleType: {self.roleType}"

    class Meta:
        db_table = 'account'
        app_label = 'account'

