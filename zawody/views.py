from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse
from django.shortcuts import render
# from .forms import ZawodyModelForm, SedziaModelForm
from django.shortcuts import redirect
from .models import Turniej, Konkurencja, Sedzia
from .forms import KonkurencjaModelForm, TurniejModelForm, SedziaModelForm
from django.urls import path
# Create your views here.


def nazwa_turnieju(arg):
	nazwa = Turniej.objects.filter(slug=arg).values_list('nazwa')
	nazwa_flat = []
	for i in nazwa:
		nazwa_flat.append(i)
	nazwa_str = ''.join(nazwa_flat[0])

	return nazwa_str

class StronaStartowaListView(ListView):
	template_name = "zawody/turniej_list_homepage.html"

	def get_queryset(self):
		return Turniej.objects.all()


def home_screen_view(request, slug):
	context = {}
	context['slug'] = slug
	context['nazwa_turnieju'] = nazwa_turnieju(slug)
	return render(request, "zawody/home.html", context)

class KonkurencjaListView(LoginRequiredMixin, ListView):
	login_url = '/start/'
	template_name = "zawody/konkurencja_lista.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context

	def get_queryset(self):
		return Konkurencja.objects.all()

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(KonkurencjaListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class KonkurencjaCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/konkurencja_create.html"
	form_class = KonkurencjaModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context

	def get_success_url(self):
		return reverse("zawody:lista_konkurencji", kwargs={'slug':self.kwargs['slug']})
		return super(KonkurencjaCreateView, self).form_valid(form)
	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(KonkurencjaCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			# return redirect("not_authorized")
			pass


class KonkurencjaDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "zawody/konkurencja_delete.html"
	context_object_name = 'zawody'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])
		return context

	def get_queryset(self):
		return Konkurencja.objects.all()

	def get_success_url(self):
		return reverse("zawody:lista_konkurencji", kwargs={'slug': self.kwargs['slug_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(KonkurencjaDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')



class TurniejListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "zawody/turniej_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context

	def get_queryset(self):
		return Turniej.objects.all()

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(TurniejListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			# pass


class TurniejCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/turniej_create.html"
	form_class = TurniejModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context

	def get_success_url(self):
		return reverse("zawody:lista_turniejow", kwargs={'slug':self.kwargs['slug']})
		return super(TurniejListView, self).form_valid(form)
	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(TurniejCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect("not_authorized")


class TurniejDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "zawody/turniej_delete.html"
	context_object_name = 'turniej'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])
		return context

	def get_queryset(self):
		return Turniej.objects.all()

	def get_success_url(self):
		return reverse("zawody:lista_turniejow", kwargs={'slug': self.kwargs['slug_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(TurniejDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class TurniejEditView(LoginRequiredMixin,UpdateView):
	login_url = 'start'
	template_name = "zawody/turniej_edit.html"
	form_class = TurniejModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])
		return context

	def get_queryset(self):
		return Turniej.objects.all()

	def get_success_url(self):
		return reverse("zawody:lista_turniejow", kwargs={'slug':self.kwargs['slug_turniej']})
		return super(TurniejEditView, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(TurniejEditView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			# pass



class SedziaListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "zawody/sedzia_lista.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context

	def get_queryset(self):
		return Sedzia.objects.all().order_by('konkurencja')

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				print(request.user.id)
				return super(SedziaListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class SedziaCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/sedzia_create.html"
	form_class = SedziaModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug'])
		return context

	def get_success_url(self):
		return reverse("zawody:sedzia_lista", kwargs={'slug': self.kwargs['slug']})
		return super(SedziaCreateView, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(SedziaCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')







class SedziaDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "zawody/sedzia_delete.html"
	context_object_name = 'sedzia'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['slug'] = self.kwargs['slug_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['slug_turniej'])

		return context

	def get_queryset(self):
		return Sedzia.objects.all()

	def get_success_url(self):
		return reverse("zawody:sedzia_lista", kwargs={'slug': self.kwargs['slug_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(SedziaDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
