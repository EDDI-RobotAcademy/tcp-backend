from rest_framework import viewsets, status
from rest_framework.response import Response

from account.repository.account_repository_impl import AccountRepositoryImpl
from account.repository.profile_repository_impl import ProfileRepositoryImpl
from account.serializers import AccountSerializer
from account.service.account_service_impl import AccountServiceImpl
from kakao_oauth.service.redis_service_impl import RedisServiceImpl


class AccountView(viewsets.ViewSet):
    accountService = AccountServiceImpl.getInstance()
    profileRepository = ProfileRepositoryImpl.getInstance()
    accountRepository = AccountRepositoryImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()

    def checkEmailDuplication(self, request):
        print("checkEmailDuplication()")

        try:
            email = request.data.get("email")
            isDuplicate = self.accountService.checkEmailDuplication(email)

            return Response(
                {
                    "isDuplicate": isDuplicate,
                    "message": (
                        "Email이 이미 존재" if isDuplicate else "Email 사용 가능"
                    ),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("이메일 중복 체크 중 에러 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def checkNicknameDuplication(self, request):
        print("checkNicknameDuplication()")

        try:
            nickname = request.data.get("newNickname")
            print(f"nickname: {nickname}")
            isDuplicate = self.accountService.checkNicknameDuplication(nickname)

            return Response(
                {
                    "isDuplicate": isDuplicate,
                    "message": (
                        "Nickname이 이미 존재" if isDuplicate else "Nickname 사용 가능"
                    ),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("닉네임 중복 체크 중 에러 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def registerAccount(self, request):
        try:
            nickname = request.data.get("nickname")
            email = request.data.get("email")
            gender = request.data.get("gender")  # 성별 추가
            birthyear = request.data.get("birthyear")  # 생년월일 추가

            account = self.accountService.registerAccount(
                loginType="KAKAO",
                roleType="NORMAL",
                nickname=nickname,
                email=email,
                gender=gender,
                birthyear=birthyear,
            )

            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("계정 생성 중 에러 발생:", e)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def getNickname(self, request):
        userToken = request.data.get("userToken")
        if not userToken:
            return Response(None, status=status.HTTP_200_OK)
        accountId = self.redisService.getValueByKey(userToken)
        profile = self.profileRepository.findById(accountId)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        nickname = profile.nickname
        return Response(nickname, status=status.HTTP_200_OK)

    def getEmail(self, request):
        userToken = request.data.get("userToken")
        if not userToken:
            return Response(None, status=status.HTTP_200_OK)
        accountId = self.redisService.getValueByKey(userToken)
        profile = self.profileRepository.findById(accountId)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        email = profile.email
        return Response(email, status=status.HTTP_200_OK)

    def withdrawAccount(self, request):
        try:
            withdrawReason = request.data.get("reason")
            print(f"reason: {withdrawReason}")

            userToken = request.data.get("userToken")
            if not userToken:
                return Response(None, status=status.HTTP_200_OK)

            accountId = self.redisService.getValueByKey(userToken)
            account = self.accountRepository.findById(accountId)
            if account is None:
                return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

            res = self.accountService.withdrawAccount(accountId, withdrawReason)
            print(f"account: {account}")
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            print("회원 탈퇴 중 에러 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def getGender(self, request):
        userToken = request.data.get("userToken")
        if not userToken:
            return Response(None, status=status.HTTP_200_OK)
        id = self.redisService.getValueByKey(userToken)
        profile = self.profileRepository.findByGender(id)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        gender = profile.gender_type
        return Response(gender, status=status.HTTP_200_OK)

    def getBirthyear(self, request):
        userToken = request.data.get("userToken")
        if not userToken:
            return Response(None, status=status.HTTP_200_OK)
        accountId = self.redisService.getValueByKey(userToken)
        profile = self.profileRepository.findById(accountId)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        birthyear = profile.birthyear
        return Response(birthyear, status=status.HTTP_200_OK)
