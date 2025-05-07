from django import forms

from app.models import MasterPemasok


class MasterPemasokForm(forms.ModelForm):
    class Meta:
        model = MasterPemasok
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alamat'] = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
