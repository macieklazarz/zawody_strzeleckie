from zawody.models import Konkurencja, Sedzia, Turniej
from django.contrib import admin

# Register your models here.
@admin.register(Turniej)
class TurniejAdmin(admin.ModelAdmin):
	list_display = ('nazwa', 'klasyfikacja_generalna', 'slug',)
	search_fields = ('nazwa',)

@admin.register(Sedzia)
class SedziaAdmin(admin.ModelAdmin):
	list_display = ('konkurencja','osoba', 'slug',)
	search_fields = ('nazwa','osoba')

@admin.register(Konkurencja)
class KonkurencjaAdmin(admin.ModelAdmin):
	list_display = ('nazwa', 'turniej', 'slug',)
	search_fields = ('nazwa','turniej',)