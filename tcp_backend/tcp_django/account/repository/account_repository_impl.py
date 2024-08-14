from account.entity.account import Account
from account.entity.account_login_type import AccountLoginType
from account.entity.account_role_type import AccountRoleType
from account.repository.account_repository import AccountRepository

from django.utils import timezone

class AccountRepositoryImpl(AccountRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self, loginType, roleType):
        loginTypeEntity = AccountLoginType.objects.get_or_create(loginType=loginType)
        roleTypeEntity = AccountRoleType.objects.get_or_create(roleType=roleType)
        loginType = loginTypeEntity[0]
        roleType = roleTypeEntity[0]

        account = Account.objects.create(loginType=loginType, roleType=roleType)
        return account

    def findById(self, accountId):
        account = Account.objects.get(id=accountId)
        return account

    # 접속시간 기록을 위한 추가
    def updateLastLogin(self, profile):
        try:
            profile.last_login = timezone.now() + timezone.timedelta(hours=9)
            profile.save()
        except Exception as e:
            print(f"최근 접속시간 업데이트 중 에러 발생: {e}")
            return None

    def withdrawAccount(self, account, withdrawReason):
        role_type = AccountRoleType.objects.get(id=account.roleType_id)

        if role_type.roleType == "NORMAL":
            role_type.roleType = "BLACKLIST"
            role_type.save()

            account.roleType = role_type
            account.withdraw_reason = withdrawReason
            account.withdraw_at = timezone.now()
            account.save()
            print('계정 탈퇴 완료')
        else:
            raise ValueError('이미 탈퇴된 계정입니다')