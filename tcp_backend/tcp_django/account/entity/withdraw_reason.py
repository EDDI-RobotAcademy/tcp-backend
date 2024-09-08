from django.db import models


class WithdrawReason(models.TextChoices):
    SERVICE_DISSATISFACTION = 'SERVICE_DISSATISFACTION'  # 서비스 품질 불만족
    LOW_USAGE = 'LOW_USAGE'  # 사용 빈도 저조
    OTHER_SERVICE = 'OTHER_SERVICE'  # 다른 서비스 사용
    PRIVACY_CONCERN = 'PRIVACY_CONCERN'  # 개인 정보 보호 우려
    OTHER = 'OTHER'  # 기타