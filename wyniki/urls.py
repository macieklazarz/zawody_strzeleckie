from django.contrib import admin
from django.urls import path, include
from .views import RejestracjaDoKonkurencjiView, OplataListView, OplataUpdateView, wyniki, exportexcel, wyniki_edycja, WynikUpdateView, WynikiDeleteView
app_name = 'wyniki'

urlpatterns = [
	path('rejestracja_do_konkurencj/<slug:slug>', RejestracjaDoKonkurencjiView.as_view(), name="rejestracja_do_konkurencj"),
	path('lista_oplat/<slug:slug>', OplataListView.as_view(), name="lista_oplat"),
	path('edytuj_oplate/<slug:slug>/<slug:slug_turniej>', OplataUpdateView.as_view(), name="edytuj_oplate"),
	path('wyniki/<slug:slug>/', wyniki, name="wyniki"),
	path('exportexcel/<slug:slug>', exportexcel, name="exportexcel"),
	path('wyniki_edycja/<slug:slug>', wyniki_edycja, name="wyniki_edycja"),
	path('edycja_wyniku/<slug:slug>/<slug:slug_turniej>', WynikUpdateView.as_view(), name="edycja_wyniku"),
	path('usuwanie_wyniku/<slug:slug>/<slug:slug_turniej>', WynikiDeleteView.as_view(), name="usuwanie_wyniku"),

	]