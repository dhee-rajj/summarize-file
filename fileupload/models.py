from django.db import models

class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255, null=True)
    file_path = models.CharField(max_length=255, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)