from django import forms
from django.forms import inlineformset_factory

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
