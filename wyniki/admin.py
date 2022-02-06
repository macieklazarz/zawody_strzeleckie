from django.contrib import admin
# from uzytkownicy.models import Uzytkownik
from wyniki.models import Wyniki

# Register your models here.
@admin.register(Wyniki)
class WynikiAdmin(admin.ModelAdmin):
	list_display = ('slug','konkurencja', 'zawodnik','oplata', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'wynik','rezultat')
	search_fields = ('konkurencja', 'zawodnik')

