from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
import xlwt
from django.views.decorators.csrf import csrf_exempt
from .forms import RejestracjaModelForm, ModuleFormSet
from .models import Wyniki
from uzytkownicy.models import Uzytkownik
from zawody.models import Konkurencja, Turniej, Sedzia
from uzytkownicy.views import nazwa_turnieju
from .forms import WynikiModelForm

# Create your views here.
def not_authorized(request):
	return render(request, 'wyniki/not_authorized.html')



class RejestracjaDoKonkurencjiView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "wyniki/rejestracja.html"
	form_class = RejestracjaModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		dodawanie_zawodnika = Turniej.objects.filter(slug=self.kwargs['slug']).values_list("rejestracja")
		for i in dodawanie_zawodnika:
			opcja = i[0]
		context['dodawanie_zawodnika'] = opcja
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		lista_zarejestrowanych = Wyniki.objects.filter(zawodnik__id = self.request.user.id).filter(konkurencja__turniej__slug = self.kwargs['slug']).values_list("konkurencja__nazwa", flat=True)
		context['lista_zarejestrowanych'] = lista_zarejestrowanych
		return context

	def get_success_url(self):
		return reverse("wyniki:rejestracja_do_konkurencj", kwargs={'slug': self.kwargs['slug']})
		return super(RejestracjaDoKonkurencjiView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(RejestracjaDoKonkurencjiView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user.is_rts})
		kwargs.update({'slug': self.kwargs['slug']})
		return kwargs

	def get_initial(self, *args, **kwargs):
		initial = super(RejestracjaDoKonkurencjiView, self).get_initial()
		initial = initial.copy()
		initial['zawodnik'] = self.request.user
		return initial


class OplataListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "wyniki/oplata_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context

	def get_queryset(self):
		return Uzytkownik.objects.all().order_by('nazwisko')

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_rts:
				return super(OplataListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')




class OplataUpdateView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url='start'
    template_name = 'wyniki/oplata_update.html'
    uzytkownik = None

    def get_formset(self, data=None, turniej=1):
        return ModuleFormSet(instance=self.uzytkownik,queryset=Wyniki.objects.filter(konkurencja__turniej__slug=turniej),
                             data=data)

    def dispatch(self, request, slug, slug_turniej):
    	try:

    		if request.user.is_rts:
    			self.uzytkownik = get_object_or_404(Uzytkownik,
		                                        slug=slug)
    			return super().dispatch(request, slug)
    		else:
    			return reverse('not_authorized')
    	except:
    		return redirect(reverse('not_authorized'))
    		# pass


    def get(self, request, *args, **kwargs):
        try:
        	formset = self.get_formset(turniej=self.kwargs['slug_turniej'])
        except:
        	print('error')
        return self.render_to_response({'uzytkownik': self.uzytkownik,
                                        'formset': formset,
                                        'slug': self.kwargs['slug_turniej'],
                                        'nazwa_turnieju': nazwa_turnieju(self.kwargs['slug_turniej'])})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST, turniej=self.kwargs['slug_turniej'])
        if formset.is_valid():
            formset.save()
            return redirect(reverse("wyniki:lista_oplat", kwargs={'slug': self.kwargs['slug_turniej']}))
        return self.render_to_response({'uzytkownik': self.uzytkownik,
                                        'formset': formset,
                                        'slug': self.kwargs['slug_turniej'],
                                        'nazwa_turnieju': nazwa_turnieju(self.kwargs['slug_turniej'])})


@login_required(login_url="/start/")
def wyniki(request, slug):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(slug)
	#robi?? list?? 'zawody_lista' zawod??w turnieju
	zawody = Konkurencja.objects.filter(turniej__slug=slug).values_list('id', flat=True).order_by('id')
	zawody_lista = []
	for i in zawody:
		zawody_lista.append(i)
	#robi?? list?? z nazwami zawod??w 'zawody_nazwa' za pomoc?? listy 'zawody_lista' 
	zawody_nazwa_queryset = Konkurencja.objects.filter(turniej__slug=slug).values_list('nazwa', flat=True).order_by('id')
	zawody_nazwa = []
	for i in zawody_nazwa_queryset:
		zawody_nazwa.append(i)

	wyniki = []
	sedziowie_queryset = []	
	sedziowie = []
	for i in zawody_lista:
		wyniki.append(Wyniki.objects.filter(konkurencja = i, oplata=1).order_by('kara', '-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))
		sedziowie_queryset.append(Sedzia.objects.filter(konkurencja = i).values_list('osoba__imie', 'osoba__nazwisko'))
	for i in sedziowie_queryset:
		sedziowie.append(i)
	context['sedziowie'] = sedziowie
	klasyfikacja_generalna = Wyniki.objects.raw('select wyniki_wyniki.id, zawodnik_id, sum(X) as X, sum(Xx) as Xx,sum(dziewiec) as dziewiec, sum(osiem) as osiem,sum(siedem) as siedem ,sum(szesc) as szesc, sum(piec) as piec, sum(cztery) as cztery, sum(trzy) as trzy, sum(dwa) as dwa, sum(jeden) as jeden, sum(wynik) as wynik from wyniki_wyniki inner join zawody_konkurencja on wyniki_wyniki.konkurencja_id = zawody_konkurencja.id inner join zawody_turniej on zawody_turniej.id = zawody_konkurencja.turniej_id where zawody_turniej.slug = %s and oplata=1 and wyniki_wyniki.kara = %s group by zawodnik_id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC, szesc desc, piec desc, cztery desc, trzy desc, dwa desc, jeden desc', [slug, 'BRAK'])
	context['wyniki'] = wyniki
	context['zawody_nazwa'] = zawody_nazwa
	context['klasyfikacja_generalna'] = klasyfikacja_generalna
	klasyfikacja_generalna_display = Turniej.objects.filter(slug=slug).values_list('klasyfikacja_generalna', flat=True)
	context['klasyfikacja_generalna_display'] = klasyfikacja_generalna_display[0]
	context['slug'] = slug

	return render(request, 'wyniki/wyniki.html', context)


@csrf_exempt
@login_required(login_url="/start/")
def wyniki_edycja(request, slug):
	if request.user.is_sedzia:
		context = {}
		context['slug'] = slug
		context['nazwa_turnieju'] = nazwa_turnieju(slug)
		turniej = Turniej.objects.filter(slug=slug).values_list('id', flat=True)
		turniej_id = turniej[0]

		#sprawdzam konkurencje przypisane do turnieju
		zawody_turnieju = Konkurencja.objects.filter(turniej=turniej_id).values_list('id', flat=True)
		zawody_turnieju_id = []
		for i in zawody_turnieju:
			zawody_turnieju_id.append(i)

		#sprawdzamy u??ytkownika ktory jest zalogowany
		user_id = request.user.id 					
		#sprawdzamy do jakich zawodow jest przyporzadkowany zalogowany user															
		powiazane_zawody = Sedzia.objects.filter(osoba__id = user_id).values_list('konkurencja', flat=True)			
		powiazane_zawody_lista = []																				
		for i in powiazane_zawody:
			if i in zawody_turnieju_id:
				powiazane_zawody_lista.append(i)

		#zapisujemy w li??cie wyniki wyniki wszystkich zawodnik??w dla poszczeg??lnych zawod??w
		wyniki = []																			
		for i in powiazane_zawody_lista:
			wynik = Wyniki.objects.filter(konkurencja = i).order_by('zawodnik__nazwisko')
			#do listy wyniki maj?? trafia?? tylko te wyniki, kt??re dotycz?? konkretnego turnieju
			#gdyby nie by??o dodatkowego filtrowania pojawia??y by si?? b????dy w przypadku gdy jedna konkurencja wyst??powa??aby w wielu turniejach
			wyniki.append(wynik.filter(konkurencja__turniej__slug=slug, oplata=1))

		#zapisujemy w li??cie zawody_nazwa nazwy zawod??w, z kt??rymi powi??zany jest s??dzia
		zawody_nazwa = []
		nazwy_zawodow = Konkurencja.objects.filter(id__in=powiazane_zawody_lista).values_list('nazwa', flat=True)
		#do listy zawody_nazwa maj?? trafia?? tylko te wyniki, kt??re dotycz?? konkretnego turnieju
		#gdyby nie by??o dodatkowego filtrowania pojawia??y by si?? b????dy w przypadku gdy jedna konkurencja wyst??powa??aby w wielu turniejach
		nazwy_zawodow = nazwy_zawodow.filter(turniej__slug=slug)
		for i in nazwy_zawodow:
			zawody_nazwa.append(i)
		context['wyniki'] = wyniki
		context['zawody_nazwa'] = zawody_nazwa
		
		return render(request, 'wyniki/edytuj_wyniki.html', context)
	else:
		return redirect('not_authorized')




class WynikUpdateView(LoginRequiredMixin, UpdateView):
	login_url = 'start'
	template_name = "wyniki/wyniki_edit.html"
	form_class = WynikiModelForm
	context_object_name = 'cont'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])
		return context

	def get_queryset(self):
		return Wyniki.objects.all()

	def get_success_url(self):
		return reverse("wyniki:wyniki_edycja", kwargs={'slug': self.kwargs['slug_turniej']})

	def form_valid(self, form):
		return super(WynikUpdateView,self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		#sprawdzam czy u??ytkownk kt??ry pr??buje edytowa?? wynik jest s??dzi?? uprawnionym do edycji wynik??w danej konkurencji. Je??li nie to przekierowuj?? do not_authorized.
		slug = self.kwargs.get('slug')
		zawody_pk = Wyniki.objects.filter(slug = slug).values_list('konkurencja__id', flat=True)
		zawody_pk_lista = []
		for i in zawody_pk:
			zawody_pk_lista.append(i)
		zawody_pk_lista = zawody_pk_lista[0]
		sedzia_pk = Sedzia.objects.filter(konkurencja__id = zawody_pk_lista).values_list('osoba__id', flat=True)
		sedzia_pk_lista = []
		for i in sedzia_pk:
			sedzia_pk_lista.append(i)
		user_id=self.request.user.id
		if user_id in sedzia_pk_lista:
			return super(WynikUpdateView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')


class WynikiDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "wyniki/konkurencja_delete.html"
	context_object_name = 'zawodnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])
		return context

	def get_queryset(self):
		return Wyniki.objects.all()

	def get_success_url(self):
		return reverse("wyniki:wyniki_edycja", kwargs={'slug': self.kwargs['slug_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(WynikiDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			# pass















@login_required(login_url="/start/")
def exportexcel(request, slug):
	if request.user.username == 'admin':
		response=HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=Wyniki_' + str(datetime.datetime.now())+'.xls'
		wb = xlwt.Workbook(encoding='utf-8')

		zawody = Konkurencja.objects.filter(turniej__slug=slug).values_list('nazwa', flat=True).order_by('id')
		ws = []
		for i in zawody:
			ws.append(wb.add_sheet(i))

		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold=True

		columns = ['Nazwisko','Imi??', 'Klub', 'X', '10', '9', '8', '7','6','5','4','3','2','1', 'Suma', 'Kara']

		for col_num in range(len(columns)):
			for i in ws:
				i.write(row_num, col_num, columns[col_num], font_style)


		font_style = xlwt.XFStyle()
		zawody_id = Konkurencja.objects.filter(turniej__slug=slug).values_list('id', flat=True).order_by('id')
		zawody_id_lista = []
		for i in zawody_id:
			zawody_id_lista.append(i)


		rows = []
		for i in zawody_id_lista:
			rows.append(Wyniki.objects.filter(konkurencja__id = i, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'wynik', 'kara').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))
		# rows.append(Wyniki.objects.filter(zawody__turniej = pk, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'wynik', 'kara').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))	
		generalka = Wyniki.objects.raw('select uzytkownicy_uzytkownik.nazwisko, uzytkownicy_uzytkownik.imie, uzytkownicy_uzytkownik.klub, sum(X) as X, sum(Xx) as Xx,sum(dziewiec) as dziewiec, sum(osiem) as osiem,sum(siedem) as siedem , sum(szesc) as szesc, sum(piec) as piec, sum(cztery) as cztery, sum(trzy) as trzy, sum(dwa) as dwa, sum(jeden) as jeden, sum(wynik) as wynik, uzytkownicy_uzytkownik.id from uzytkownicy_uzytkownik inner join zawody_konkurencja on wyniki_wyniki.konkurencja_id = zawody_konkurencja.id inner join wyniki_wyniki on uzytkownicy_uzytkownik.id=wyniki_wyniki.zawodnik_id inner join zawody_turniej on zawody_turniej.id = zawody_konkurencja.turniej_id where zawody_turniej.slug = %s and oplata=1 and wyniki_wyniki.kara = %s group by uzytkownicy_uzytkownik.id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC', [slug, 'BRAK'])
		# generalka = Wyniki.objects.raw('select wyniki_wyniki.id, zawodnik_id, sum(X) as X, sum(Xx) as Xx,sum(dziewiec) as dziewiec, sum(osiem) as osiem,sum(siedem) as siedem , sum(szesc) as szesc, sum(piec) as piec, sum(cztery) as cztery, sum(trzy) as trzy, sum(dwa) as dwa, sum(jeden) as jeden, sum(wynik) as wynik from wyniki_wyniki inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.turniej_id = %s and oplata=1 and wyniki_wyniki.kara = %s group by zawodnik_id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC', [pk, 'BRAK'])
		# rows.append(generalka)
		for x,y in enumerate(ws):
			row_num = 0
			for row in rows[x]:
				row_num +=1
				for col_num in range(len(row)):
					y.write(row_num, col_num, str(row[col_num]), font_style)



		ws.append(wb.add_sheet("Klasyfikacja generalna"))
		columns = ['Nazwisko','Imi??', 'Klub', 'X', '10', '9', '8', '7','6','5','4','3','2','1', 'Suma']
		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold=True
		for col_num in range(len(columns)):
				ws[len(ws)-1].write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()
		zakladka_klasyfikacja_generalna = len(ws)-1
		for i,y in enumerate(generalka):
			ws[zakladka_klasyfikacja_generalna].write(i+1, 0, y.nazwisko, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 1, y.imie, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 2, y.klub, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 3, y.X, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 4, y.Xx, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 5, y.dziewiec, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 6, y.osiem, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 7, y.siedem, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 8, y.szesc, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 9, y.piec, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 10, y.cztery, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 11, y.trzy, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 12, y.dwa, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 13, y.jeden, font_style)
			ws[zakladka_klasyfikacja_generalna].write(i+1, 14, y.wynik, font_style)


		wb.save(response)

		return(response)

	else:
		return redirect('start')