# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(label='Usuario', max_length=20)
	password = forms.CharField(label=u'Contraseña', widget=forms.PasswordInput)