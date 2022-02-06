from django.contrib import admin
from django.urls import path, include
from.views import logout_view, login_view, registration_form, registration_form_sedzia, registration_form_no_login, UzytkownicyListView, UzytkownicyUpdateView, UzytkownicyDeleteView, PasswordResetViewNew, PasswordResetDoneViewNew, PasswordResetConfirmViewNew, PasswordResetCompleteViewNew
app_name = 'uzytkownicy'

urlpatterns = [
	path('<slug:slug>/', logout_view, name="logout"),
	path('login/<slug:slug>', login_view, name="login"),
	path('register/<slug:slug>', registration_form, name="register"),
	path('register_sedzia/<slug:slug>', registration_form_sedzia, name="register_sedzia"),
	path('uzytkownicy_lista/<slug:slug>', UzytkownicyListView.as_view(), name="uzytkownicy_lista"),
    path('edytuj_uzytkownika/<slug:slug>/<slug:slug_turniej>', UzytkownicyUpdateView.as_view(), name="edytuj_uzytkownika"),
	path('usun_uzytkownika/<slug:slug>/<slug:slug_turniej>',UzytkownicyDeleteView.as_view(), name="usun_uzytkownika"),
    path('register_no_login/<slug:slug>', registration_form_no_login, name="register_no_login"),


    path('<slug:slug>/password_reset/',
        PasswordResetViewNew.as_view(),
        name="password_reset"),
    path('<slug:slug>/password_reset/done/',
        PasswordResetDoneViewNew.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        PasswordResetConfirmViewNew.as_view(),
        name='password_reset_confirm'),
    path('reset/done/',
        PasswordResetCompleteViewNew.as_view(),
        name='password_reset_complete'),

	]