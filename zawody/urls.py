from django.contrib import admin
from django.urls import path, include
from.views import home_screen_view, KonkurencjaListView, KonkurencjaCreateView, KonkurencjaDeleteView, TurniejListView, TurniejCreateView, TurniejDeleteView, TurniejEditView, SedziaListView, SedziaCreateView, SedziaDeleteView
app_name = 'zawody'

urlpatterns = [
	path('<int:pk>/', home_screen_view, name="home"),
	path('lista_konkurencji/<int:pk>', KonkurencjaListView.as_view(), name="lista_konkurencji"),
	path('dodaj_konkurencje/<int:pk>', KonkurencjaCreateView.as_view(), name="dodaj_konkurencje"),
	path('usun_konkurencje/<int:pk>/<int:pk_turniej>', KonkurencjaDeleteView.as_view(), name="usun_konkurencje"),
	path('lista_turniejow/<int:pk>', TurniejListView.as_view(), name="lista_turniejow"),
	path('dodaj_turniej/<int:pk>', TurniejCreateView.as_view(), name="dodaj_turniej"),
    path('edytuj_turniej/<int:pk>/<int:pk_turniej>', TurniejEditView.as_view(), name="edytuj_turniej"),
    path('usun_turniej/<int:pk>/<int:pk_turniej>', TurniejDeleteView.as_view(), name="usun_turniej"),
    path('sedzia_lista/<int:pk>', SedziaListView.as_view(), name="sedzia_lista"),
    path('dodaj_sedziego/<int:pk>', SedziaCreateView.as_view(), name="dodaj_sedziego"),
	path('usun_sedziego/<int:pk_turniej>/<int:pk>',SedziaDeleteView.as_view(), name="usun_sedziego"),



	]