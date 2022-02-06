from django.db import models
from uzytkownicy.models import Uzytkownik
from django.utils.text import slugify


class Turniej(models.Model):
	nazwa = models.CharField(max_length=30, unique=True)
	rejestracja = models.BooleanField(verbose_name='Rejestracja')
	slug = models.SlugField(unique=True)
	klasyfikacja_generalna = models.BooleanField(default=True, verbose_name='Klasyfikacja generalna')


	def save(self, *args, **kwargs):
		self.slug = slugify(self.nazwa)
		super(Turniej, self).save(*args, **kwargs)

	def __str__(self):
		return self.nazwa
	class Meta:
		verbose_name_plural = "Turnieje"

class Konkurencja(models.Model):
	nazwa = models.CharField(max_length=30)
	liczba_strzalow = models.IntegerField(default=10)
	turniej = models.ForeignKey(Turniej, on_delete=models.CASCADE, null=True)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(str(self.turniej)+"_"+str(self.nazwa))
		super(Konkurencja, self).save(*args, **kwargs)

	def __str__(self):
		return self.nazwa

	class Meta:
		verbose_name_plural = "Konkurencja"
		unique_together =('nazwa','turniej',)

#nazwakonkurencji i turniej powinny być unikalne


class Sedzia(models.Model):
	konkurencja	= models.ForeignKey(Konkurencja, on_delete=models.CASCADE)
	osoba 		= models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
	slug 		= models.SlugField()

	def save(self, *args, **kwargs):
		self.slug = slugify(str(self.konkurencja)+"_"+str(self.osoba))
		super(Sedzia, self).save(*args, **kwargs)



	class Meta:
		verbose_name_plural = "Sędziowie"