from django import forms

from terima_barang.models import TerimaBarang


class TerimaBarangForm(forms.ModelForm):
    class Meta:
        model = TerimaBarang
        fields = '__all__'
