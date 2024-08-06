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
        loginTypeEntity = AccountLoginType.objects.create(loginType=loginType)
        roleTypeEntity = AccountRoleType.objects.create(roleType=roleType)

        account = Account.objects.create(loginType=loginTypeEntity, roleType=roleTypeEntity)
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

