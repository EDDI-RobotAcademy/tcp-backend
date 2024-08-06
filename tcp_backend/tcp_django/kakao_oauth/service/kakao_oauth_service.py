from abc import ABC, abstractmethod

class KakaoOauthService(ABC):

    @abstractmethod
    def kakaoLoginAddress(self):
        pass

    @abstractmethod
    def requestAccessToken(self, kakaoAuthCode):
        pass

    @abstractmethod
    def requestUserInfo(self, accessToken):
        pass