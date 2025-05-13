from django.db import models

from barang.models import MasterBarang
from preorder.models import PreOrder


class TerimaBarang(models.Model):
    nomor_terima = models.CharField(max_length=255, unique=True)
    tanggal = models.DateField()
    preorder = models.ForeignKey(PreOrder, on_delete=models.CASCADE, related_name='preorder')

    def __str__(self):
        return f'{self.nomor_terima} - {self.tanggal}'


class TerimaBarangDetail(models.Model):
    terima_barang = models.ForeignKey(TerimaBarang, on_delete=models.CASCADE, related_name='terima_barang_detail')
    kode_barang = models.ForeignKey(MasterBarang, on_delete=models.CASCADE)
    qty_terima = models.IntegerField()
