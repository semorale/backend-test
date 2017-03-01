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



