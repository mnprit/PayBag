from django.shortcuts import redirect
from datetime import datetime
from .models import *
from django.contrib import messages
import sys
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from Customer.models import *
from Supplier.models import *

def checklogin(function):
	def  wrap(request, *args, **kwargs):
		try:
			print('checklogin decorator for API')
			print(request.POST)
			session_token_val = request.POST.get('session_token')
			print(session_token_val)
			if session_token_val:
				obj=MainUser.objects.filter(token=session_token_val)
				if obj:
					pass
				else:
					print('1')
					return JsonResponse({ 'code': 0 , 'error': 'User not logged in.','status_code': 0 , 'status_message': 'User not logged in.' }, status=404, safe=False)
			else:
				print('2')
				return JsonResponse({ 'code': 0 , 'error': 'User not logged in.','status_code': 0 , 'status_message': 'User not logged in.' }, status=404, safe=False)
			return function(request, *args, **kwargs)
		except Exception as e:
			print(e)
			return JsonResponse({ 'code': 0 , 'error': str(e),'status_code': 0 , 'status_message': str(e) }, status=404, safe=False)
	wrap.__doc__ = function.__doc__
	# wrap.__name__ = function.__name__
	return wrap

def checksupplierlogin(function):
	def  wrap(request, *args, **kwargs):
		try:
			session_token_val = request.POST.get('session_token')
			if session_token_val:
				obj=Supplier.objects.filter(token=session_token_val)
				if obj:
					pass
				else:
					return JsonResponse({ 'code': 0 , 'error': 'User not logged in.', }, status=404, safe=False)
			else:
				return JsonResponse({ 'code': 0 , 'error': 'User not logged in.', }, status=404, safe=False)
			return function(request, *args, **kwargs)
		except Exception as e:
			print(e)
	wrap.__doc__ = function.__doc__
	# wrap.__name__ = function.__name__
	return wrap
