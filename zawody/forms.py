from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Konkurencja, Turniej, Sedzia


class KonkurencjaModelForm(forms.ModelForm):
	class Meta:
		model = Konkurencja
		fields = (
			'nazwa',
			'liczba_strzalow',
			'turniej',
			)
	def __init__(self, *args, **kwargs):
		super(KonkurencjaModelForm, self).__init__(*args, **kwargs)
		self.fields['liczba_strzalow'].label = 'Liczba strzałów'



class TurniejModelForm(forms.ModelForm):
    class Meta:
        model = Turniej
        fields = (
            'nazwa',
            'rejestracja',
            )

#formularz przypisywania sędziego do konkurencji
class SedziaModelForm(forms.ModelForm):
	class Meta:
		model = Sedzia
		fields = (
			'konkurencja',
			'osoba',
			)
	def __init__(self, *args, **kwargs):
		super(SedziaModelForm, self).__init__(*args, **kwargs)
		#w propertce sedzia możemy wybrać tylko takiego usera, który jest sędzią lub rtsem
		self.fields['osoba'].queryset = self.fields['osoba'].queryset.filter(is_sedzia=1) | self.fields['osoba'].queryset.filter(is_rts=1)
		self.fields['osoba'].label = 'Sędzia'