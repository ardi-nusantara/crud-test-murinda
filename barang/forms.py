from django import forms
from barang.models import MasterBarang


class MasterBarangForm(forms.ModelForm):
    class Meta:
        model = MasterBarang
        fields = '__all__'
