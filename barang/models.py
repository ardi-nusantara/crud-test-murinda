from django.core.exceptions import ValidationError
from django.db import models

from app.choices import MASTER_BARANG_TYPES, MASTER_BARANG_LEVELS


class MasterBarang(models.Model):
    kode = models.CharField(max_length=255, unique=True)
    nama = models.CharField(max_length=255)
    tipe = models.CharField(choices=MASTER_BARANG_TYPES)
    level = models.CharField(choices=MASTER_BARANG_LEVELS)
    induk = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    satuan = models.CharField(max_length=255, blank=True, null=True)
    harga = models.IntegerField(blank=True, null=True)
    qtystok = models.IntegerField()

    def __str__(self):
        return f'{self.kode} - {self.nama}'

    def clean(self):
        # Custom validation for the 'induk' field
        if self.induk and self.induk.level >= self.level:
            raise ValidationError('The referenced induk must have a smaller level than the current object.')
