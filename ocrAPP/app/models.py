from django.db import models
# from .models import CustomAuthUser  # Replace with the actual path to your CustomAuthUser model

class Document(models.Model):
    UPLOAD_CHOICES = (
        ('png', 'PNG'),
        ('jpg', 'JPEG'),
        ('pdf', 'PDF'),
    )

    file = models.FileField(upload_to='documents/')
    format = models.CharField(max_length=4, choices=UPLOAD_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name

class ExportedDocument(models.Model):
    EXPORT_CHOICES = (
        ('txt', 'TXT'),
        ('doc', 'DOC'),
    )

    file = models.FileField(upload_to='exported_documents/')
    format = models.CharField(max_length=3, choices=EXPORT_CHOICES)
    exported_at = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name