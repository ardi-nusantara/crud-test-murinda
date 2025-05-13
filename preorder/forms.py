from django import forms

from barang.models import MasterBarang
from preorder.models import PreOrder, PreOrderDetail


class PreorderForm(forms.ModelForm):
    class Meta:
        model = PreOrder
        fields = '__all__'


class PreorderDetailForm(forms.ModelForm):
    class Meta:
        model = PreOrderDetail
        fields = '__all__'
        widgets = {
            'preorder': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = MasterBarang.objects.filter(tipe='D')
        self.fields['kode_barang'].queryset = queryset
