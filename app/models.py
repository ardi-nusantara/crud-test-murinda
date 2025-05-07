from django.db import models


class MasterPemasok(models.Model):
    kode = models.CharField(max_length=255, unique=True)
    nama = models.CharField(max_length=255)
    alamat = models.TextField()

    def __str__(self):
        return f'{self.kode} - {self.nama}'
