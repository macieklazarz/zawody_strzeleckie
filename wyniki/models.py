from django.core.exceptions import ValidationError
from django.db import models
from uzytkownicy.models import Uzytkownik
from zawody.models import Konkurencja
from django.utils.text import slugify
class Wyniki(models.Model):

	KARA_CHOICES = (
		('BRAK', 'BRAK'),
		('DNF', 'DNF'),
		('DNS', 'DNS'),
		('DSQ', 'DSQ'),
		('PK', 'PK'),
	)

	konkurencja = models.ForeignKey(Konkurencja, on_delete=models.CASCADE, verbose_name='konkurencja')
	zawodnik 	= models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
	slug 		= models.SlugField()
	X			=models.IntegerField(blank=True, null=False, default=0)
	Xx			=models.IntegerField(blank=True, null=False, default=0, verbose_name='10')
	dziewiec	=models.IntegerField(blank=True, null=False, default=0, verbose_name='9')
	osiem		=models.IntegerField(blank=True, null=False, default=0, verbose_name='8')
	siedem		=models.IntegerField(blank=True, null=False, default=0, verbose_name='7')
	szesc		=models.IntegerField(blank=True, null=False, default=0, verbose_name='6')
	piec		=models.IntegerField(blank=True, null=False, default=0, verbose_name='5')
	cztery		=models.IntegerField(blank=True, null=False, default=0, verbose_name='4')
	trzy		=models.IntegerField(blank=True, null=False, default=0, verbose_name='3')
	dwa			=models.IntegerField(blank=True, null=False, default=0, verbose_name='2')
	jeden		=models.IntegerField(blank=True, null=False, default=0, verbose_name='1')
	wynik 		=models.IntegerField(blank=True, default=0)
	rezultat	=models.TextField(max_length=60, null=True, default='0')
	kara		=models.CharField(max_length=10, choices=KARA_CHOICES, default='BRAK')
	oplata		= models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "Wyniki"
# Create your models here.
	def save(self, *args, **kwargs):
		self.slug = slugify(str(self.konkurencja)+"_"+str(self.zawodnik))
		self.wynik = self.X*10 + self.Xx*10 + self.dziewiec*9 + self.osiem*8 + self.siedem*7 + self.szesc*6+ self.piec*5+ self.cztery*4+ self.trzy*3+ self.dwa*2+ self.jeden*1

		liczba_strzalow = self.X*10 + self.Xx*10 + self.dziewiec+ self.osiem + self.siedem + self.szesc+ self.piec+ self.cztery+ self.trzy+ self.dwa+ self.jeden

		self.rezultat = str(self.X*10 + self.Xx*10 + self.dziewiec*9 + self.osiem*8 + self.siedem*7 + self.szesc*6+ self.piec*5+ self.cztery*4+ self.trzy*3+ self.dwa*2+ self.jeden*1)
		if self.kara not in ['BRAK', 'PK']:
			self.rezultat = self.kara
			self.X=0
			self.Xx=0
			self.dziewiec=0
			self.osiem=0
			self.siedem=0
			self.szesc=0
			self.piec=0
			self.cztery=0
			self.trzy=0
			self.dwa=0
			self.jeden=0
			self.wynik=0
		if self.rezultat == 'PK':
			self.rezultat = self.kara
			self.wynik = 0

		super(Wyniki, self).save(*args, **kwargs)

	def clean(self):
		liczba_strzalow = self.konkurencja.liczba_strzalow
		mozliwe_wyniki = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		if (self.X not in mozliwe_wyniki):
			raise ValidationError({'X': "Uzupełnij  pole wartością od 0 do 10"})
		elif (self.Xx not in mozliwe_wyniki):
			raise ValidationError({'Xx': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.dziewiec not in mozliwe_wyniki):
			raise ValidationError({'dziewiec': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.osiem not in mozliwe_wyniki):
			raise ValidationError({'osiem': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.siedem not in mozliwe_wyniki):
			raise ValidationError({'siedem': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.szesc not in mozliwe_wyniki):
			raise ValidationError({'szesc': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.piec not in mozliwe_wyniki):
			raise ValidationError({'piec': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.cztery not in mozliwe_wyniki):
			raise ValidationError({'cztery': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.trzy not in mozliwe_wyniki):
			raise ValidationError({'trzy': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.dwa not in mozliwe_wyniki):
			raise ValidationError({'dwa': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.jeden not in mozliwe_wyniki):
			raise ValidationError({'jeden': "Uzupełnij pole wartością od 0 do 10"})
		elif self.X+self.Xx+self.dziewiec+self.osiem+self.siedem+self.szesc+self.piec+self.cztery+self.trzy+self.dwa+self.jeden > liczba_strzalow:
			raise ValidationError({'X': f'Maksymalna liczba strzałów w tej konkurencji to {liczba_strzalow}'})


