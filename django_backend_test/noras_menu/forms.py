# -*- encoding: utf-8 -*-

#STDLIB importa
from datetime import date

#Core Django Imports
from django import forms
from django.forms.models import inlineformset_factory
#Third Party apps imports

#Imports local apps
from .models import Menu, MenuItems, UserSelectedLunch, Subscribers

class MenuForm(forms.ModelForm):
	day = forms.DateField(label='Menu date', input_formats=['%d-%m-%Y'])

	class Meta:
		model = Menu
		fields = '__all__'

MenuItemsFormSet = inlineformset_factory(Menu, MenuItems, fields=('name','menu',))

class MenuSelectForm(forms.ModelForm):

	class Meta:
		model = UserSelectedLunch
		fields = '__all__'

class SubscribersForm(forms.ModelForm):

	class Meta:
		model = Subscribers
		fields = '__all__'