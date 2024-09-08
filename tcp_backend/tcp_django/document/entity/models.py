from django.db import models

class Document(models.Model):
    documentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, null=False)
    writer = models.CharField(max_length=32, null=False)
    file = models.FileField(upload_to='documents/')
    content = models.TextField()
    regDate = models.DateTimeField(auto_now_add=True)
    updDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'document'
