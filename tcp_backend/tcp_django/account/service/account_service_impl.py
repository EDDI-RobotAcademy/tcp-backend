from account.repository.account_repository_impl import AccountRepositoryImpl
from account.repository.profile_repository_impl import ProfileRepositoryImpl
from account.service.account_service import AccountService



class AccountServiceImpl(AccountService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__profileRepository = ProfileRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def checkEmailDuplication(self, email):
        profile = self.__profileRepository.findByEmail(email)
        return profile is not None

    def checkNicknameDuplication(self, nickname):
        profile = self.__profileRepository.findByNickname(nickname)
        return profile is not None

    def registerAccount(self, loginType, roleType, nickname, email, gender, birthyear):
        account = self.__accountRepository.create(loginType, roleType)
        return self.__profileRepository.create(nickname, email, gender, birthyear, account)

    def findAccountByEmail(self, email):
        profile = self.__profileRepository.findByEmail(email)
        if profile:
            self.__profileRepository.updateLastLogin(profile)
            self.__profileRepository.update_login_history(profile)
        return profile
    
