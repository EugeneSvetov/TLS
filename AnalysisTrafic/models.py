from django.db import models



class File(models.Model):
    title = models.CharField(max_length=150)
    file_csv = models.FileField(upload_to='csv/')

    def __str__(self):
        return self.title
