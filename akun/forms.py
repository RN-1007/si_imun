from django import forms
from .models import JadwalImunisasi

class JadwalImunisasiForm(forms.ModelForm):
    class Meta:
        model = JadwalImunisasi
        fields = ['jenis_imunisasi', 'tanggal', 'keterangan']
        labels = {
            'jenis_imunisasi': 'Jenis Imunisasi',
            'tanggal': 'Tanggal Imunisasi',
            'keterangan': 'Keterangan Tambahan',
        }
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
        }