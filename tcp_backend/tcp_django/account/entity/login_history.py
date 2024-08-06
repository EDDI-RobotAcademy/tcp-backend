from django.db import models


class LoginHistory(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.IntegerField()
    login_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if 'force_login_at' in kwargs:
            self._meta.get_field('login_at').auto_now = False
            self.login_at = kwargs.pop('force_login_at')
        super().save(*args, **kwargs)
        if 'force_login_at' not in kwargs:
            self._meta.get_field('login_at').auto_now = True

    def __str__(self):
        return f"LoginHistory -> account_id: {self.account_id}, login_at: {self.login_at}"

    class Meta:
        db_table = 'account_login_history'
        app_label = 'account'