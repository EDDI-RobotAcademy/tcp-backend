from django.db import models



class AccountRoleType(models.Model):
    class RoleType(models.TextChoices):
        ADMIN = 'ADMIN'
        NORMAL = 'NORMAL'
        BLACKLIST = 'BLACKLIST'
        
    roleType = models.CharField(max_length=64, choices=RoleType.choices, default=RoleType.NORMAL, unique=True)

    def __str__(self):
        return self.roleType

    class Meta:
        db_table = 'account_role_type'
        app_label = 'account'