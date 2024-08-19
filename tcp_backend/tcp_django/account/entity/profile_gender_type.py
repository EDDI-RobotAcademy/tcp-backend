from django.db import models


class ProfileGenderType(models.Model):
    class GenderType(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'

    gender_type = models.CharField(max_length=10, choices=GenderType.choices, unique=True)

    def __str__(self):
        return self.gender_type
    
    class Meta:
        db_table = 'profile_gender_type'
        app_label = 'account'