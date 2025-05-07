from django import forms

from preorder.models import PreOrder


class PreorderForm(forms.ModelForm):
    class Meta:
        model = PreOrder
        fields = '__all__'
