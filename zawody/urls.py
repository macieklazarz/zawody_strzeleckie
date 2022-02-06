from django.contrib import admin
from django.urls import path, include
from.views import home_screen_view, KonkurencjaListView, KonkurencjaCreateView, KonkurencjaDeleteView, TurniejListView, TurniejCreateView, TurniejDeleteView, TurniejEditView, SedziaListView, SedziaCreateView, SedziaDeleteView
app_name = 'zawody'

urlpatterns = [
	path('<slug:slug>/', home_screen_view, name="home"),
	path('lista_konkurencji/<slug:slug>', KonkurencjaListView.as_view(), name="lista_konkurencji"),
	path('dodaj_konkurencje/<slug:slug>', KonkurencjaCreateView.as_view(), name="dodaj_konkurencje"),
	path('usun_konkurencje/<slug:slug>/<slug:slug_turniej>', KonkurencjaDeleteView.as_view(), name="usun_konkurencje"),
	path('lista_turniejow/<slug:slug>', TurniejListView.as_view(), name="lista_turniejow"),
	path('dodaj_turniej/<slug:slug>', TurniejCreateView.as_view(), name="dodaj_turniej"),
    path('edytuj_turniej/<slug:slug>/<slug:slug_turniej>', TurniejEditView.as_view(), name="edytuj_turniej"),
    path('usun_turniej/<slug:slug>/<slug:slug_turniej>', TurniejDeleteView.as_view(), name="usun_turniej"),
    path('sedzia_lista/<slug:slug>', SedziaListView.as_view(), name="sedzia_lista"),
    path('dodaj_sedziego/<slug:slug>', SedziaCreateView.as_view(), name="dodaj_sedziego"),
	path('usun_sedziego/<slug:slug>/<slug:slug_turniej>',SedziaDeleteView.as_view(), name="usun_sedziego"),



	]