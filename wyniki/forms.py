from django import forms
from . import models
from wyniki.models import Wyniki
from django.core.exceptions import ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from django.forms.models import inlineformset_factory
from zawody.models import Konkurencja
from uzytkownicy.models import Uzytkownik

class RejestracjaModelForm(forms.ModelForm):
    class Meta:
        model = Wyniki
        fields = (
            'konkurencja',
            'zawodnik',
            )

    def clean(self):
        cleaned_data = super().clean()
        wybrane_zawody = cleaned_data.get('konkurencja').id                                                                                                           #sprawdzam jakie wybrano zawody
        wybrany_zawodnik = cleaned_data.get('zawodnik').id                                                                                                       #sprawdzam jakiego wybrano zawodnika (tu zostanie przypisany mail)

        # print(f'zawody to {wybrane_zawody}')
        # print(f'zawodnik to {wybrany_zawodnik}')

        zawodnicy_przypisani_do_zawodow = Wyniki.objects.filter(konkurencja__id=wybrane_zawody).values_list('zawodnik', flat=True).distinct()                          #wybieram wszystkich zawodników którzy są przypisani do wybranych zawodów (zmienna wybrane_zawody)
        zawodnicy_przypisani_do_zawodow_lista = []
        for i in zawodnicy_przypisani_do_zawodow:
            # print(f' wybrane zawody {i}')
            zawodnicy_przypisani_do_zawodow_lista.append(i)                                                                                                          #robię listę z wsyztskich zawodników przypisanych do danych zawodow
        print(f'zawodnicy przypisani do zawodow to {zawodnicy_przypisani_do_zawodow_lista}')
        if (wybrany_zawodnik in zawodnicy_przypisani_do_zawodow_lista):                                                                               #sprawdzam czy wybrany zawodnik jest na liscie z mailami uczestnikow wybranych zawodow
            raise ValidationError("Jesteś już zarejestrowany na te zawody")
            self.fields['zawodnik'] =wybrany_zawodnik

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        user = kwargs.pop('user', None)
        slug = kwargs.pop('slug', None)
        super(RejestracjaModelForm, self).__init__(*args, **kwargs)
        print(f'user admin to {user}')
        self.fields['konkurencja'].queryset = Konkurencja.objects.filter(turniej__slug=slug)
        self.fields['zawodnik'].queryset = Uzytkownik.objects.all().order_by('nazwisko')
        # self.fields['zawodnik'] = forms.ModelChoiceField(queryset=Account.objects.all())
        if not user:
            self.fields['zawodnik'].widget = HiddenInput()

class WynikiModelForm(forms.ModelForm):
    CHOICE= [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    ]
    X = forms.CharField(widget=forms.Select(choices=CHOICE))
    Xx = forms.CharField(widget=forms.Select(choices=CHOICE), label='10')
    dziewiec = forms.CharField(widget=forms.Select(choices=CHOICE))
    osiem = forms.CharField(widget=forms.Select(choices=CHOICE))
    siedem = forms.CharField(widget=forms.Select(choices=CHOICE))
    szesc = forms.CharField(widget=forms.Select(choices=CHOICE))
    piec = forms.CharField(widget=forms.Select(choices=CHOICE))
    cztery = forms.CharField(widget=forms.Select(choices=CHOICE))
    trzy = forms.CharField(widget=forms.Select(choices=CHOICE))
    dwa = forms.CharField(widget=forms.Select(choices=CHOICE))
    jeden = forms.CharField(widget=forms.Select(choices=CHOICE))
    class Meta:
        model = Wyniki
        fields = ['X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden','kara']

ModuleFormSet = inlineformset_factory(Uzytkownik,
                                      Wyniki,
                                      fields=['oplata',],
                                      extra=0,
                                      can_delete=False,
                                      labels = {'oplata': 'Opłata',}
                                      )