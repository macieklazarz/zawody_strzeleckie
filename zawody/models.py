from django.db import models
from uzytkownicy.models import Uzytkownik


class Turniej(models.Model):
	nazwa = models.CharField(max_length=30)
	rejestracja = models.BooleanField(verbose_name='Rejestracja')

	def __str__(self):
		return self.nazwa
	class Meta:
		verbose_name_plural = "Turnieje"

class Konkurencja(models.Model):
	nazwa = models.CharField(max_length=30)
	liczba_strzalow = models.IntegerField(default=10)
	turniej = models.ForeignKey(Turniej, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.nazwa

	class Meta:
		verbose_name_plural = "Konkurencja"


class Sedzia(models.Model):
	konkurencja	= models.ForeignKey(Konkurencja, on_delete=models.CASCADE)
	osoba 		= models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)


	class Meta:
		verbose_name_plural = "Sędziowie"