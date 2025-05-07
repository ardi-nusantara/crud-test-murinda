from django import forms

from gudang.models import MasterGudang


class MasterGudangForm(forms.ModelForm):
    class Meta:
        model = MasterGudang
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alamat'] = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
