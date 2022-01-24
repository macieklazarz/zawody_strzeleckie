from django.contrib import admin
from django.urls import path, include
from .views import RejestracjaDoKonkurencjiView, OplataListView, OplataUpdateView, wyniki, exportexcel, wyniki_edycja, WynikUpdateView
app_name = 'wyniki'

urlpatterns = [
	path('rejestracja_do_konkurencj/<int:pk>', RejestracjaDoKonkurencjiView.as_view(), name="rejestracja_do_konkurencj"),
	path('lista_oplat/<int:pk>', OplataListView.as_view(), name="lista_oplat"),
	path('edytuj_oplate/<int:pk>/<int:pk_turniej>', OplataUpdateView.as_view(), name="edytuj_oplate"),
	path('wyniki/<int:pk>/', wyniki, name="wyniki"),
	path('exportexcel/<int:pk>', exportexcel, name="exportexcel"),
	path('wyniki_edycja/<int:pk>', wyniki_edycja, name="wyniki_edycja"),
	path('edycja_wyniku/<int:pk>/<int:pk_turniej>', WynikUpdateView.as_view(), name="edycja_wyniku"),

	]