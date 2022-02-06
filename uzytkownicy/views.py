from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth import views as auth_views
from zawody.views import nazwa_turnieju
from .forms import AccountAuthenticationForm, RegistrationForm, RegistrationFormSedzia, UzytkownikModelForm, SedziaModelForm
from .models import Uzytkownik
# biblioteki do funkcji registration_form
from zawody_strzeleckie import settings
import urllib
import json
import urllib.request
from django.contrib import messages
##############################

def logout_view(request, slug):
	logout(request)
	return redirect('zawody:home', slug)

def login_view(request, slug):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(slug)
	user = request.user
	if user.is_authenticated:
		return redirect("zawody:home")
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("zawody:home", slug)
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	context['slug'] = slug
	return render(request, 'account/login.html', context)



def registration_form(request, slug):
	context={}
	context['slug'] = slug
	context['nazwa_turnieju'] = nazwa_turnieju(slug)
	if request.POST:
		form=RegistrationForm(request.POST)
		if form.is_valid():
			print('jest is valid')
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,'response': recaptcha_response}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			if result['success']:
				form.save()
				messages.success(request, 'New comment added with success!')
				email = form.cleaned_data.get('email')
				raw_password = form.cleaned_data.get('password1')
				account = authenticate(email=email, password=raw_password)
				login(request, account)
				return redirect('zawody:home', slug)
			else:
				print(' nie ma success')
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)



def registration_form_no_login(request,slug):
	if request.user.is_rts:
		context={}
		context['slug'] = slug
		context['nazwa_turnieju'] = nazwa_turnieju(slug)
		if request.POST:
			form=RegistrationForm(request.POST)
			if form.is_valid():
				form.save()
				email = form.cleaned_data.get('email')
				raw_password = form.cleaned_data.get('password1')
				account = authenticate(email=email, password=raw_password)
				return redirect('uzytkownicy:uzytkownicy_lista', slug)
			else:
				context['registration_form'] = form
		else:
			form = RegistrationForm()
			context['registration_form'] = form
		return render(request, 'account/register.html', context)
	else:
		return redirect('not_authorized')


def registration_form_sedzia(request, slug):
	context={}
	context['slug'] = slug
	context['nazwa_turnieju'] = nazwa_turnieju(slug)
	if request.POST:
		form=RegistrationFormSedzia(request.POST)
		if form.is_valid():
			print('jest is valid')
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,'response': recaptcha_response}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			if result['success']:
				form.save()
				messages.success(request, 'New comment added with success!')
				email = form.cleaned_data.get('email')
				raw_password = form.cleaned_data.get('password1')
				account = authenticate(email=email, password=raw_password)
				login(request, account)
				return redirect('zawody:home', slug)
			else:
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationFormSedzia()
		context['registration_form'] = form
	return render(request, 'account/register_sedzia.html', context)

class UzytkownicyListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "account/account_list.html"

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
				return super(UzytkownicyListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			

class UzytkownicyUpdateView(LoginRequiredMixin, UpdateView):
	login_url = 'start'
	template_name = "account/account_update.html"
	form_class = UzytkownikModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])
		return context

	def get_queryset(self):
		return Uzytkownik.objects.all()

	def get_success_url(self):
		return reverse("uzytkownicy:uzytkownicy_lista", kwargs={'slug': self.kwargs['slug_turniej']})
		
	def form_valid(self, form):
		return super(UzytkownicyUpdateView,self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_rts:
				return super(UzytkownicyUpdateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			# pass

class SedziaUpdateView(LoginRequiredMixin, UpdateView):
	login_url = 'start'
	template_name = "account/account_update.html"
	form_class = SedziaModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])
		return context

	def get_queryset(self):
		return Uzytkownik.objects.all()

	def get_success_url(self):
		return reverse("zawody:sedzia_lista", kwargs={'slug': self.kwargs['slug_turniej']})
		
	def form_valid(self, form):
		return super(SedziaUpdateView,self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_rts:
				return super(SedziaUpdateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
		   # pass
			return redirect('not_authorized')


class UzytkownicyDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "account/account_delete.html"
	context_object_name = 'zawodnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])
		return context

	def get_queryset(self):
		return Uzytkownik.objects.all()

	def get_success_url(self):
		return reverse("uzytkownicy:uzytkownicy_lista", kwargs={'slug': self.kwargs['slug_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_rts:
				return super(UzytkownicyDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class PasswordResetViewNew(auth_views.PasswordResetView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context
	def get_success_url(self):
		return reverse("uzytkownicy:password_reset_done", kwargs={'slug': self.kwargs['slug']})


class PasswordResetDoneViewNew(auth_views.PasswordResetDoneView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context

class PasswordResetConfirmViewNew(auth_views.PasswordResetConfirmView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class PasswordResetCompleteViewNew(auth_views.PasswordResetCompleteView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context