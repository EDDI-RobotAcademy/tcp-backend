import uuid

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.service.account_service_impl import AccountServiceImpl
from kakao_oauth.serializer.kakao_oauth_access_token_serializer import KakaoOauthAccessTokenSerializer
from kakao_oauth.serializer.kakao_oauth_url_serializer import KakaoOauthUrlSerializer
from kakao_oauth.service.kakao_oauth_service_impl import KakaoOauthServiceImpl
from kakao_oauth.service.redis_service_impl import RedisServiceImpl


class OauthView(viewsets.ViewSet):
    kakaoOauthService = KakaoOauthServiceImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()

    def kakaoOauthURI(self, request):
            url = self.kakaoOauthService.kakaoLoginAddress()
            print(f"url:", url)
            serializer = KakaoOauthUrlSerializer(data={ 'url': url })
            serializer.is_valid(raise_exception=True)
            print(f"validated_data: {serializer.validated_data}")
            return Response(serializer.validated_data)

    def kakaoAccessTokenURI(self, request):
        serializer = KakaoOauthAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        try:
            accessToken = self.kakaoOauthService.requestAccessToken(code)
            print(f"accessToken: {accessToken}")
            return JsonResponse({'accessToken': accessToken})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def kakaoUserInfoURI(self, request):
        accessToken = request.data.get('access_token')
        print(f'accessToken: {accessToken}')

        try:
            user_info = self.kakaoOauthService.requestUserInfo(accessToken)
            return JsonResponse({'user_info': user_info})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def redisAccessToken(self, request):
        try:
            email = request.data.get('email')
            print(f"redisAccessToken -> email: {email}")
            account = self.accountService.findAccountByEmail(email)
            if not account:
                return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

            userToken = str(uuid.uuid4())
            print(f"type of account.id: {type(account.id)}")
            self.redisService.store_access_token(account.id, userToken)
            # key로 value 찾기 테스트
            accountId = self.redisService.getValueByKey(userToken)
            print(f"accountId: {accountId}")

            return Response({ 'userToken': userToken }, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error storing access token in Redis:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def dropRedisTokenForLogout(self, request):
        try:
            userToken = request.data.get('userToken')
            isSuccess = self.redisService.deleteKey(userToken)

            return Response({'isSuccess': isSuccess}, status=status.HTTP_200_OK)
        except Exception as e:
            print('레디스 토큰 해제 중 에러 발생:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)