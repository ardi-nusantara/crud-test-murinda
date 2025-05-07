from django.db import models

from app.models import MasterPemasok
from barang.models import MasterBarang
from gudang.models import MasterGudang


class PreOrder(models.Model):
    nomor_po = models.CharField(max_length=255, unique=True)
    tanggal = models.DateField()
    pemasok = models.ForeignKey(MasterPemasok, on_delete=models.CASCADE)
    gudang = models.ForeignKey(MasterGudang, on_delete=models.CASCADE)
    kode_barang = models.ForeignKey(MasterBarang, on_delete=models.CASCADE)
    qty_po = models.IntegerField()
    harga = models.IntegerField()
    qty_terima = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.nomor_po} - {self.tanggal}'
