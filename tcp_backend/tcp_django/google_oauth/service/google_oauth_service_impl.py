from google_oauth.service.google_oauth_service import GoogleOauthService
from tcp_django import settings


import requests

class GoogleOauthServiceImpl(GoogleOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.loginUrl = settings.GOOGLE['LOGIN_URL']
            cls.__instance.clientId = settings.GOOGLE['CLIENT_ID']
            cls.__instance.clientSecret = settings.GOOGLE['CLIENT_SECRET']
            cls.__instance.redirectUri = settings.GOOGLE['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.GOOGLE['TOKEN_REQUEST_URI']
            cls.__instance.userinfoRequestUri = settings.GOOGLE['USERINFO_REQUEST_URI']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def googleLoginAddress(self):
        print("googleLoginAddress()")
        return (f"{self.loginUrl}/oauth2/v2/auth?"
                f"client_id={self.clientId}&redirect_uri={self.redirectUri}&response_type=code&scope=email")


    def requestAccessToken(self, googleAuthCode):
        print("requestAccessToken()")
        accessTokenRequestForm = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'redirect_uri': self.redirectUri,
            'code': googleAuthCode,
            'grant_type': 'authorization_code'
        }

        print(f"client_id: {self.clientId}")
        print(f"redirect_uri: {self.redirectUri}")
        print(f"code: {googleAuthCode}")
        print(f"tokenRequestUri: {self.tokenRequestUri}")

        response = requests.post(self.tokenRequestUri, data=accessTokenRequestForm)
        print(f"response content: {response.content}")

        return response.json()

    def requestUserInfo(self, accessToken):
        headers = {'Authorization': f'Bearer {accessToken}'}
        response = requests.post(self.userinfoRequestUri, headers=headers)

        print(f"response content: {response.content}")

        return response.json()




