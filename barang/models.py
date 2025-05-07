from django.db import models

from app.choices import MASTER_BARANG_TYPES, MASTER_BARANG_LEVELS


class MasterBarang(models.Model):
    kode = models.CharField(max_length=255, unique=True)
    nama = models.CharField(max_length=255)
    tipe = models.CharField(choices=MASTER_BARANG_TYPES)
    level = models.CharField(choices=MASTER_BARANG_LEVELS)
    induk = models.CharField(max_length=255, blank=True, null=True)
    satuan = models.CharField(max_length=255, blank=True, null=True)
    harga = models.IntegerField(blank=True, null=True)
    qtystok = models.IntegerField()

    def __str__(self):
        return f'{self.kode} - {self.nama}'
