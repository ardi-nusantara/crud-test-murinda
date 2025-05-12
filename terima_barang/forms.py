from django import forms

from preorder.models import PreOrder
from terima_barang.models import TerimaBarang


class TerimaBarangForm(forms.ModelForm):
    class Meta:
        model = TerimaBarang
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = PreOrder.objects.filter(qty_po__gte=1)
        self.fields['preorder'].queryset = queryset
