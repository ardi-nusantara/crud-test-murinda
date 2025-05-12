from django.db import models

from preorder.models import PreOrder


class TerimaBarang(models.Model):
    nomor_terima = models.CharField(max_length=255, unique=True)
    tanggal = models.DateField()
    preorder = models.ForeignKey(PreOrder, on_delete=models.CASCADE, related_name='preorder')
    kode_barang = models.CharField(max_length=255)
    qty_terima = models.IntegerField()

    def __str__(self):
        return f'{self.nomor_terima} - {self.tanggal}'
