# -*- encoding: utf-8 -*-

#STDLIB importa
import requests
from datetime import datetime

#Core Django Imports
from django.views.generic.edit import CreateView
from django.views.generic import  View,ListView,UpdateView
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse,reverse_lazy
from django.forms import formset_factory
#Third Party apps imports
import simplejson as json
import pytz

#Imports local apps
from .models import Menu, MenuItems, UserSelectedLunch, Subscribers
from .forms import MenuForm, MenuItemsFormSet, MenuSelectForm, SubscribersForm
from tasks import mail_remainder,slack_remainder


class CreateMenu(CreateView):
	model = Menu
	form_class = MenuForm
	template_name = 'menu_add.html'

	def dispatch(self, request, *args, **kwargs):
	    """ Permission check for this class """
	    if not request.user.has_perm('noras_menu.add_menu'):
	        raise PermissionDenied(
	            "You do not have permission"
	        )
	    return super(CreateMenu, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""
		Handles GET requests and instantiates blank versions of the form
		and its inline formsets.
		"""
		#resultado = send_email_options.delay()
		#slack_remainder()
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		menu_items_formset = MenuItemsFormSet()
		return self.render_to_response(
            self.get_context_data(form=form,
                                  menu_items_formset=menu_items_formset))

	def post(self, request, *args, **kwargs):
		"""
		Handles POST requests, instantiating a form instance and its inline
		formsets with the passed POST variables and then checking them for
		validity.
		"""
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		menu_items_formset = MenuItemsFormSet(self.request.POST)
		if (form.is_valid() and menu_items_formset.is_valid()):
		    return self.form_valid(form, menu_items_formset)
		else:
		    return self.form_invalid(form, menu_items_formset)

	def form_valid(self, form, menu_items_formset):
		"""
		Called if all forms are valid. Creates a Recipe instance along with
		associated Ingredients and Instructions and then redirects to a
		success page.
		"""
		self.object = form.save()
		menu_items_formset.instance = self.object
		menu_items_formset.save()
		link = str(self.request.get_host())+str(reverse_lazy('noras_menu:Create Selection',  kwargs = {'uuid': self.object.menu_uuid}))
		if self.request.POST.get('slack'):
			slack_remainder.delay(self.object,link)
		if self.request.POST.get('mail'):
			mail_remainder.delay(self.object, link)
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, menu_items_formset):
		"""
		Called if a form is invalid. Re-renders the context data with the
		data-filled forms and errors.
		"""
		return self.render_to_response(
		    self.get_context_data(form=form,
		                          menu_items_formset=menu_items_formset))

	def get_success_url(self):
		return reverse('noras_menu:Create Menu')


class ListMenu(ListView):
	model = Menu
	template_name = 'menu_list.html'

	def dispatch(self, request, *args, **kwargs):
	    """ Permission check for this class """
	    if not request.user.has_perm('noras_menu.list_menu'):
	        raise PermissionDenied(
	            "You do not have permission"
	        )
	    return super(ListMenu, self).dispatch(request, *args, **kwargs)


class UpdateMenu(UpdateView):
	model = Menu
	template_name = 'menu_edit.html'
	fields = ['day','id']

	def dispatch(self, request, *args, **kwargs):
	    """ Permission check for this class """
	    if not request.user.has_perm('noras_menu.change_menu'):
	        raise PermissionDenied(
	            "You do not have permission"
	        )
	    return super(UpdateMenu, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse_lazy('noras_menu:Update Menu',  kwargs = {'pk': self.object.pk})

	def get(self, request, *args, **kwargs):
		"""
		Handles GET requests and instantiates blank versions of the form
		and its inline formsets.
		"""
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		menu_items_formset = MenuItemsFormSet(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form,menu_items_formset=menu_items_formset))

	def post(self, request, *args, **kwargs):
		"""
		Handles POST requests, instantiating a form instance and its inline
		formsets with the passed POST variables and then checking them for
		validity.
		"""
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		menu_items_formset = MenuItemsFormSet(self.request.POST, instance=self.object)
		if (form.is_valid() and menu_items_formset.is_valid()):
		    return self.form_valid(form, menu_items_formset)
		else:
		    return self.form_invalid(form, menu_items_formset)

	def form_valid(self, form, menu_items_formset):
		"""
		Called if all forms are valid. Creates a Recipe instance along with
		associated Ingredients and Instructions and then redirects to a
		success page.
		"""
		self.object = form.save()
		menu_items_formset.instance = self.object
		menu_items_formset.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, menu_items_formset):
		"""
		Called if a form is invalid. Re-renders the context data with the
		data-filled forms and errors.
		"""
		return self.render_to_response(
		    self.get_context_data(form=form,
		                          menu_items_formset=menu_items_formset))


class CreateSelection(CreateView):
	model = UserSelectedLunch
	form_class = MenuSelectForm
	template_name = 'menu_select.html'

	def get(self, request, *args, **kwargs):
		if 'uuid' in kwargs:
			uuid = kwargs['uuid']
			menu = get_object_or_404(Menu, menu_uuid = uuid)
		menu_date_naive = datetime.combine(menu.day, datetime.strptime('11:00AM', '%I:%M%p').time())
		deadline = pytz.timezone('America/Santiago').localize(menu_date_naive)
		my_date = datetime.now(pytz.timezone('America/Santiago'))
		if my_date > deadline:
			return HttpResponse("Menu Closed for this Day")
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		items = MenuItems.objects.filter(menu_id=menu.pk)
		print items

		return render_to_response(self.get_template_names(),{'form':form, 'menu':menu.pk, 'uuid':uuid, 'menu_items':items}, RequestContext(request))

	def post(self, request, *args, **kwargs):
		"""
		Handles POST requests, instantiating a form instance and its inline
		formsets with the passed POST variables and then checking them for
		validity.
		"""
		if 'uuid' in kwargs:
			uuid = kwargs['uuid']
			menu = get_object_or_404(Menu, menu_uuid = uuid)
		menu_date_naive = datetime.combine(menu.day, datetime.strptime('11:00AM', '%I:%M%p').time())
		deadline = pytz.timezone('America/Santiago').localize(menu_date_naive)
		my_date = datetime.now(pytz.timezone('America/Santiago'))
		if my_date > deadline:
			return HttpResponse("Menu Closed for this Day")
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
		    return self.form_valid(form)
		else:
		    return self.form_invalid(form)

	def get_success_url(self):
		return reverse_lazy('noras_menu:Create Selection',  kwargs = {'uuid': self.kwargs['uuid']})

class ListSelection(ListView):
	""" Simple list of selected menu order by day"""
	model = UserSelectedLunch
	template_name = "menu_list_selected.html"

	def dispatch(self, request, *args, **kwargs):
	    """ Permission check for this class """
	    if not request.user.has_perm('noras_menu.list_selected'):
	        raise PermissionDenied(
	            "You do not have permission"
	        )
	    return super(ListSelection, self).dispatch(request, *args, **kwargs)


class CreateSubscriber(CreateView):
	""" View to add a subscriber to de db"""
	model = Subscribers
	form_class = SubscribersForm
	template_name = "menu_add_subscriber.html"

	def get_success_url(self):
		return reverse_lazy('noras_menu:Create Subscriber')
