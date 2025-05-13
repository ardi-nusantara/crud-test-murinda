from django import forms

from preorder.models import PreOrder, PreOrderDetail
from terima_barang.models import TerimaBarang, TerimaBarangDetail


class TerimaBarangForm(forms.ModelForm):
    class Meta:
        model = TerimaBarang
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = PreOrder.objects.filter(preorder_detail__kode_barang__qtystok__gte=1).distinct()
        self.fields['preorder'].queryset = queryset


class TerimaBarangDetailForm(forms.ModelForm):
    class Meta:
        model = TerimaBarangDetail
        fields = '__all__'
        widgets = {
            'terima_barang': forms.HiddenInput(),
        }
