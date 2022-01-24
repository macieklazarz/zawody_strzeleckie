from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from uzytkownicy.models import Uzytkownik



# Register your models here.

class UzytkownikAdmin(UserAdmin):
	list_display = ('email', 'username','nazwisko', 'imie', 'date_joined', 'last_login', 'is_admin', 'is_rts')
	search_fields = ('email', 'username', 'nazwisko')
	readonly_field = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Uzytkownik, UzytkownikAdmin)