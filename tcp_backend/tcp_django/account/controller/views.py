import hashlib
import os
import uuid
import random
import string

from dotenv import load_dotenv
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

    load_dotenv()

    def checkEmailDuplication(self, request):
        print("checkEmailDuplication()")

        try:
            print(f"request.data: {request.data}")
            email = request.data.get("email")
            print(f"email: {email}")
            isDuplicate = self.accountService.checkEmailDuplication(email)
            print(f"isDuplicate: {isDuplicate}")

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
            password = request.data.get("password")
            gender = request.data.get("gender")  # 성별 추가
            birthyear = request.data.get("birthyear")  # 생년월일 추가
            loginType = request.data.get("loginType")

            randomString = string.ascii_letters + string.digits + string.punctuation
            salt = ''.join(random.choice(randomString) for _ in range(16))

            encodedPassword = salt.encode("utf-8") + password.encode("utf-8")
            hashedPassword = hashlib.sha256(encodedPassword)
            password = hashedPassword.hexdigest()

            if loginType == "NORMAL":
                account = self.accountService.registerAccount(
                    loginType=loginType,
                    roleType="NORMAL",
                    nickname=nickname,
                    email=email,
                    password=password,
                    salt=salt,
                    gender=gender,
                    birthyear=birthyear,
                )
            else:
                account = self.accountService.registerAccount(
                    loginType=loginType,
                    roleType="NORMAL",
                    nickname=nickname,
                    email=email,
                    password=None,
                    salt=None,
                    gender=gender,
                    birthyear=birthyear,
                )

            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("계정 생성 중 에러 발생:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def getNickname(self, request):
        email = request.data.get("email")
        if not email:
            return Response(None, status=status.HTTP_200_OK)
        profile = self.profileRepository.findByEmail(email)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        nickname = profile.nickname
        return Response(nickname, status=status.HTTP_200_OK)

    # def getEmail(self, request):
    #     userToken = request.data.get("userToken")
    #     if not userToken:
    #         return Response(None, status=status.HTTP_200_OK)
    #     accountId = self.redisService.getValueByKey(userToken)
    #     profile = self.profileRepository.findById(accountId)
    #     if profile is None:
    #         return Response(
    #             {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
    #         )  # 에러 처리 추가
    #     email = profile.email
    #     return Response(email, status=status.HTTP_200_OK)

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
        email = request.data.get("email")
        if not email:
            return Response(None, status=status.HTTP_200_OK)
        profile = self.profileRepository.findByEmail(email)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        genderId = profile.gender_id
        profileGenderType = self.profileRepository.findGenderTypeByGenderId(genderId)
        genderType = profileGenderType.gender_type
        return Response(genderType, status=status.HTTP_200_OK)

    def getBirthyear(self, request):
        email = request.data.get("email")
        if not email:
            return Response(None, status=status.HTTP_200_OK)
        profile = self.profileRepository.findByEmail(email)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        birthyear = profile.birthyear
        return Response(birthyear, status=status.HTTP_200_OK)

    def checkNormalLogin(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            profile = self.profileRepository.findByEmail(email)

            if not profile:
                isEmailCollect = False
                isPasswordCollect = False
                return Response({"isEmailCollect": isEmailCollect,
                                 "isPasswordCollect": isPasswordCollect,
                                 "message": '존재하지 않는 이메일'},
                                status=status.HTTP_200_OK,)

            encodedPassword = profile.salt.encode("utf-8") + password.encode("utf-8")
            hashedPassword = hashlib.sha256(encodedPassword)
            password = hashedPassword.hexdigest()

            isEmailCollect = True
            isPasswordCollect = True if password == profile.password else False
            return Response(
                {"isEmailCollect": isEmailCollect,
                    "isPasswordCollect": isPasswordCollect,
                    "message": (
                        "비밀번호 일치" if isPasswordCollect else "비밀번호가 일치하지 않음"
                    ),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("비밀번호 확인 중 에러 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
