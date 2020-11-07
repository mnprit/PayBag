# coding=utf-8
from django.shortcuts import render
from passlib.hash import django_pbkdf2_sha256 as handler
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from Customer.models import *
from Supplier.models import *
from BasicPages.models import *
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import os,binascii
from rest_framework.authtoken.models import Token
import smtplib, ssl
from django.conf import settings
import random,string
import datetime
from datetime import timedelta
import math, random 
from django.core.files.storage import FileSystemStorage
from Mobileapis.serializers import *
from Mobileapis.decorators import *
from django.utils.decorators import method_decorator
from django.db.models import Q
from dateutil.parser import parse
from django.conf import settings
from SuperAdmin.models import *
from pyfcm import FCMNotification
# from Delivery.models import *
from django.views.generic.base import TemplateView

import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pyqrcode 
from pyqrcode import QRCode 
				
import pdfkit
from headless_pdfkit import generate_pdf
import pytz	
import boto3
from django.core.mail import EmailMultiAlternatives

from currency_converter import CurrencyConverter
from django.core.mail import send_mail
import calendar
import os

from SuperAdmin.send_mail_from_adminsection_template import parcel_delivered_success_mail, payment_reminder_mail # for testing purpose only

from BasicPages.basic_pages_functions import getcourierprice_easyship, generate_awbpdf, generate_paymentreceiptpdf,convertuserbalance, getcourierpricefrombackend, convert_currency_between_countries, getawbfilepath, getpaymentreceiptfilepath, getatnfilepath, getunreadnotificationscount, deliverygetunreadnotificationscount
from SuperAdmin.send_mail_from_adminsection_template import gettimezone, getcurrenttimeinnewcountrytimezone, convertutctonewtimezone, jaadu
#testing purpose 

class filterTraveller(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		try:
			print("one")
			des_city = request.POST.get('toCity')
			print("two")
			if not des_city:
				return Response({'code': 400,'status':'false','message': 'Destination City is required'})	
			city = request.POST.get('fromCity')
			print("two")
			if not city:
				return Response({'code': 400,'status':'false','message': 'City is required'})
			start_date = request.POST.get('searchDate')
			print("three")
			if not start_date:
				return Response({'code': 400,'status':'false','message': 'Date is required'})
			# time = request.POST.get('searchTime')
			# print("three")
			# if not time:
			# 	return Response({'code': 400,'status':'false','message': 'Time is required'})
			# print("four")
			time='00:00:00'	
			start_date = start_date.split('-')
			start_date = str(start_date[1])+'/'+str(start_date[2])+'/'+str(start_date[0])
			start_date = parse(start_date)
			print("five")
			print('before main_user_obj')
			print("==================here from enterd date")
			dep_time = parse(time).time()
			print(dep_time)

			departuredatetime = datetime.datetime.combine(start_date.date(),dep_time)
			print(type(departuredatetime))
			print(departuredatetime)
			main_user_obj = SupplierJob.objects.filter(Q(tocity=des_city)&Q(fromcity=city))
			# print('after main_user_obj')
			# print("six")
			print(main_user_obj)
			timeuser='not'
			print("==================here from new date")
			alluser=[]
			for user in main_user_obj:
				print(type(user.departuretime))
				new_time = user.departuretime
				print(new_time)
				newdate=user.departuredate
				newdeparturedatetime = datetime.datetime.combine(newdate,new_time)
				print(type(newdeparturedatetime))
				print(newdeparturedatetime)
				if(newdeparturedatetime>=departuredatetime):
					image=''
					if not user.user.user.image.name:
						image=''
					else:
						if '//' in user.user.user.image.name:
							print('full url exists')
							image = user.user.user.image.name
							image = image.replace('original','200*200')
						else:
							image = str(settings.WEB_BASE_URL)+'media/200*200-'+user.user.user.image.name
					alluser.append({'ID':user.traveller_id,
						             'Name':user.user.user.name,
						             'Phone':user.user.user.phone,
						             'Departure Time':user.departuretime,
						             'Arrival Time':user.arrivaltime,
						             'Rating':2,
						             'Completed Task':0,
						             'Profile Picture':image,
						             'Charges per KG':user.chrgesperkg,
						             'From Country':user.fromcountry,
						             'From City':user.fromcity,
						             'Departure Date':user.departuredate,
						             'To country':user.tocountry,
						             'To city':user.tocity,
						             'Arrival Date':user.arrivaldate,
						             'Travel By':user.travel_by
						           })
			print(alluser)
			if main_user_obj:
				return Response({'code': 200,'status':'true','message': 'Travller Find','List':alluser})
			else:
				print("seven")
				return Response({'code': 200,'status':'true','message': 'Travller Not Find','List':alluser})
		except Exception as e:
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})

@method_decorator(checklogin, name='dispatch')
class DeleteParcelRequest(APIView):
	# permission_classes = (IsAuthenticated,)
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		session_token_val = request.POST.get('session_token')
		# parcel_id_val = request.POST.get('parcel_id')
		if not session_token_val:
			return Response({'code': 0, 'error': 'Session Token Empty',})
		Request_id = request.POST.get('RequestId')
		if not Request_id:
			return Response({'code': 0, 'error': 'Request Id is Required',})
		a=[]
		ids=[]
		main_job_obj=MainUser.objects.filter(token=session_token_val)
		if not main_job_obj:
			return Response({'code': 0, 'error': 'User Not Logged IN',})
			a.append('yes')
		customerObj=Customer.objects.filter(user=main_job_obj[0])
		if not customerObj:
			return Response({'code': 0, 'error': 'User Not Register as Tav eller',})
			a.append('yes')
		data=[]
		customerjobobj=CustomerJob.objects.filter(user=customerObj[0],parcel_id=Request_id)
		if customerjobobj:
			# customerjobobj.requestAccept=False
			customerjobobj.deleteRequest=True
			return Response({'code': 200, 'message': 'Delete Request',})
		else:
			return Response({'code': 0, 'message': 'No Reuest Find'})

@method_decorator(checklogin, name='dispatch')
class RejectParcelRequest(APIView):
	# permission_classes = (IsAuthenticated,)
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		session_token_val = request.POST.get('session_token')
		# parcel_id_val = request.POST.get('parcel_id')
		if not session_token_val:
			return Response({'code': 0, 'error': 'Session Token Empty',})
		Request_id = request.POST.get('RequestId')
		if not Request_id:
			return Response({'code': 0, 'error': 'Request Id is Required',})
		a=[]
		ids=[]
		main_job_obj=MainUser.objects.filter(token=session_token_val)
		if not main_job_obj:
			return Response({'code': 0, 'error': 'User Not Logged IN',})
			a.append('yes')
		supplier_obj_job=Supplier.objects.filter(user=main_job_obj[0])
		if not supplier_obj_job:
			return Response({'code': 0, 'error': 'User Not Register as Tav eller',})
			a.append('yes')
		data=[]
		customerjobobj=CustomerJob.objects.filter(travller=supplier_obj_job[0],parcel_id=Request_id)
		if customerjobobj:
			customerjobobj.requestAccept=False
			customerjobobj.requestReject=True
			return Response({'code': 200, 'message': 'Request Rejected Successfully',})
		else:
			return Response({'code': 0, 'message': 'No Reuest Find'})
		return Response({'code': 0, 'data': data,})

@method_decorator(checklogin, name='dispatch')
class AcceptParcelRequest(APIView):
	# permission_classes = (IsAuthenticated,)
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		session_token_val = request.POST.get('session_token')
		# parcel_id_val = request.POST.get('parcel_id')
		if not session_token_val:
			return Response({'code': 0, 'error': 'Session Token Empty',})
		Request_id = request.POST.get('RequestId')
		if not Request_id:
			return Response({'code': 0, 'error': 'Request Id is Required',})
		charges = request.POST.get('Charges')
		if not charges:
			return Response({'code': 0, 'error': 'Please Add Charges',})
		a=[]
		ids=[]
		main_job_obj=MainUser.objects.filter(token=session_token_val)
		if not main_job_obj:
			return Response({'code': 0, 'error': 'User Not Logged IN',})
			a.append('yes')
		supplier_obj_job=Supplier.objects.filter(user=main_job_obj[0])
		if not supplier_obj_job:
			return Response({'code': 0, 'error': 'User Not Register as Taveller',})
			a.append('yes')
		data=[]
		customerjobobj=CustomerJob.objects.filter(travller=supplier_obj_job[0],parcel_id=Request_id)
		if customerjobobj:
			customerjobobj[0].requestAccept=True
			customerjobobj[0].requestReject=False
			customerjobobj[0].chargesByTraveller=charges
			customerjobobj[0].save()
			return Response({'code': 200, 'message': 'Request Accept Successfully',})
		else:
			return Response({'code': 0, 'message': 'No Reuest Find'})

@method_decorator(checklogin, name='dispatch')
class ShowAllRequestsToCustomer(APIView):
	# permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		session_token_val = request.POST.get('session_token')
		main_user_obj=MainUser.objects.filter(token=session_token_val)
		if not main_user_obj:
			return JsonResponse({ 'code': 200 , 'message' : 'User Not Logged In'})
		customerObj=Customer.objects.filter(user=main_user_obj[0])
		if not customerObj:
			return JsonResponse({ 'code': 200 , 'message' : 'User Not Registerd as Customer'})
		Customerobj=CustomerJob.objects.filter(user=customerObj[0])
		reqData=[]
		if not Customerobj:
			return JsonResponse({ 'code': 200 , 'message' : 'No Sending Request of Parcel'})
		if Customerobj:
			for custom in Customerobj:
				if custom.requestAccept:
					reqData.append({'Charges By Traveller':custom.chargesByTraveller})
					# ChargesByTraveller=custom.chargesByTraveller
				if custom.requestSend:
					reqData.append({'Request Send':'True'})
				else:
					reqData.append({'Request Send':'False'})
				if custom.requestAccept:
					reqData.append({'Request Accept':'True'})
				else:
					reqData.append({'Request Accept':'False'})
				if custom.requestReject:
					reqData.append({'Request Rejected':'True'})
				else:
					reqData.append({'Request Rejected':'False'})
				if custom.requestPaid:
					reqData.append({'Request Paid':'True'})
				else:
					reqData.append({'Request Paid':'False'})
				reqData.append({
					'Traveller':custom.travller.user.name,
					'User':custom.user.user.name,
					'Parcel Id':custom.parcel_id,
					'Pickup Address':custom.pickupaddress,
					'From Country':custom.fromcountry,
					'From City':custom.fromcity,
					'Postal Code':custom.frompostalcode,
					
					'Reciver Name':custom.receivername,
					'Reciver Country Code':custom.receivercountrycode,
					'Reciver Phone':custom.receiverphone,
					'Reciver Drop Address':custom.receiverdropaddress,
					
					'Reacive To Country':custom.tocountry,
					'Reacive City':custom.tocity,
					'Reacive Postal code':custom.topostalcode,
					
					'Weight':custom.parcelweight,
					
					'Description':custom.description,
					'Date':custom.job_creation_date,
					'Job Satatus':custom.job_status,
					# :custom.requestSend
					# :custom.requestAccept
					# :custom.requestReject
					# :custom.requestPaid
					# :custom.chargesByTraveller

					})
			return JsonResponse({ 'code': 200 ,'Request Status':reqData})
			serializer = CustomerJobSerializer(Customerobj, many=True)
			print(serializer.data)
			return JsonResponse({ 'code': 200 ,'Request Status':reqData,'data' : serializer.data }, status=200, safe=False)
		try:
			print(Customerobj)
		except Exception as e:
			print(e)
		
		if Customerobj:
			pass
			serializer = CustomerJobSerializer(Customerobj, many=True)
			print(serializer.data)
			return JsonResponse({ 'code': 200 ,'Request Status':reqData, 'data' : serializer.data }, status=200, safe=False)


@method_decorator(checklogin, name='dispatch')
class notificationTravellerAndCustomer(APIView):
	# permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		session_token_val = request.POST.get('session_token')
		try:
			main_user_obj=MainUser.objects.filter(token=session_token_val)
			if not main_user_obj:
				return JsonResponse({ 'code': 0 , 'message' : 'User Not Logged In'})
			travellerObj=Supplier.objects.filter(user=main_user_obj[0])
			customerObj=Customer.objects.filter(user=main_user_obj[0])
			all_request=[]
			travelFinder=True
			customerFinder=True
			if not travellerObj:
				travelFinder=False
				# all_request.append({'AsTraveller':'No Request As Travller'})
				# all_request.append({'TravellingRequest':False})
			if not customerObj:
				customerFinder=False
				# all_request.append({'AsCustomer':'No Request As Customer'})
				# all_request.append({'CustomerRequest':False})
			forFunExtra=True
			if forFunExtra:
				if travelFinder and customerFinder:
					Customerobj=CustomerJob.objects.filter(Q(travller=travellerObj[0])|Q(user=customerObj[0]))
				else:
					if travelFinder:
						Customerobj=CustomerJob.objects.filter(Q(travller=travellerObj[0]))
					if customerFinder:
						Customerobj=CustomerJob.objects.filter(Q(user=customerObj[0]))
				# if not customerObj:
				# 	all_request.append({'AsCustomer':'No Request As Customer'})
				# 	all_request.append({'CustomerRequest':False})
				# Customerobj=CustomerJob.objects.filter(Q(travller=travellerObj[0])|Q(user=customerObj[0]))
				if Customerobj:
					for custom in Customerobj:
						if travelFinder:
							if custom.travller==travellerObj[0]:
								if custom.requestAccept==True or custom.requestReject ==True :
									pass
								else:
									if not custom.travller.user.image.name:
										image=''
									else:
										if '//' in custom.travller.user.image.name:
											print('full url exists')
											image = custom.travller.user.image.name
											image = image.replace('original','200*200')
										else:
											image = str(settings.WEB_BASE_URL)+'media/200*200-'+custom.travller.user.image.name
									all_request.append({
										'statusId':'Traveller',
										'Traveller Name':custom.travller.user.name,
										'User Name':custom.user.user.name,
										'User Phone':custom.user.user.phone,
										'Parcel Id':custom.parcel_id,
										'Pickup Address':custom.pickupaddress,
										'From Country':custom.fromcountry,
										'From City':custom.fromcity,
										'Postal Code':custom.frompostalcode,
										
										'Reciver Name':custom.receivername,
										'Reciver Country Code':custom.receivercountrycode,
										'Reciver Phone':custom.receiverphone,
										'Reciver Drop Address':custom.receiverdropaddress,
										
										'Reaciver Country':custom.tocountry,
										'Reaciver City':custom.tocity,
										# 'Reacive Postal code':custom.topostalcode,
										
										'Weight':custom.parcelweight,
										
										'Description':custom.description,
										'Date':custom.job_creation_date,
										'Job Satatus':custom.job_status,
										'requestSend':custom.requestSend,
										'requestAccept':custom.requestAccept,
										'requestReject':custom.requestReject,
										'requestPay':custom.requestPaid,
										'image':image,
										})
						if customerFinder:
							if custom.user==customerObj[0]:
								if not custom.travller.user.image.name:
									image=''
								else:
									if '//' in custom.travller.user.image.name:
										print('full url exists')
										image = custom.travller.user.image.name
										image = image.replace('original','200*200')
									else:
										image = str(settings.WEB_BASE_URL)+'media/200*200-'+custom.travller.user.image.name
								all_request.append({
									'statusId':'Sender',
									'Traveller Name':custom.travller.user.name,
									'User Name':custom.user.user.name,
									'User Phone':custom.user.user.phone,
									'Parcel Id':custom.parcel_id,
									'Pickup Address':custom.pickupaddress,
									'From Country':custom.fromcountry,
									'From City':custom.fromcity,
									'Postal Code':custom.frompostalcode,
									
									'Reciver Name':custom.receivername,
									'Reciver Country Code':custom.receivercountrycode,
									'Reciver Phone':custom.receiverphone,
									'Reciver Drop Address':custom.receiverdropaddress,
									
									'Reaciver Country':custom.tocountry,
									'Reaciver City':custom.tocity,
									# 'Reacive Postal code':custom.topostalcode,
									
									'Weight':custom.parcelweight,
									
									'Description':custom.description,
									'Date':custom.job_creation_date,
									'Job Satatus':custom.job_status,
									'requestSend':custom.requestSend,
									'requestAccept':custom.requestAccept,
									'requestReject':custom.requestReject,
									'requestPay':custom.requestPaid,
									'image':image,
									})
				else:
					return JsonResponse({'message':'No Request Found'})
			return JsonResponse({ 'code': 200 , 'data' : all_request})
		except Exception as e:
			return JsonResponse({ 'code': 0 , 'message' : e})
		# 		serializer = CustomerJobSerializer(Customerobj, many=True)
		# 		print(serializer.data)
		# 		all_request.append({'AsTraveller':serializer.data})
		# 		all_request.append({'TravellingRequest':True})
		# 		all_request.append({'isTraveller':True})
		# 		# return JsonResponse({ 'code': 200 , 'AsTraveller' : serializer.data }, status=200, safe=False)
		# 	else:
		# 		all_request.append({'AsTraveller':'No Request As Travller'})
		# 		all_request.append({'TravellingRequest':False})

		
		# if not customerObj:
		# 	all_request.append({'AsCustomer':'No Request As Customer'})
		# 	all_request.append({'CustomerRequest':False})	
		# else:
		# 	Customerobj=CustomerJob.objects.filter(user=customerObj[0])
		# 	if Customerobj:
		# 		serializer = CustomerJobSerializer(Customerobj, many=True)
		# 		print(serializer.data)
		# 		all_request.append({'AsCustomer':serializer.data})
		# 		all_request.append({'CustomerRequest':True})
		# 		# return JsonResponse({ 'code': 200 , 'AsTraveller' : serializer.data }, status=200, safe=False)
		# 	else:
		# 		all_request.append({'AsCustomer':'No Request As Customer'})
		# 		all_request.append({'CustomerRequest':False})	
		# return JsonResponse({ 'code': 200 , 'data' : all_request})
		# try:
		# 	print(Customerobj)
		# except Exception as e:
		# 	print(e)
		# reqData=[]
		# if Customerobj:
		# 	if Customerobj.requestSend:
		# 		reqData.append({'Request Send':'True'})
		# 	else:
		# 		reqData.append({'Request Send':'False'})
		# 	if Customerobj.requestAccept:
		# 		reqData.append({'Request Accept':'True'})
		# 	else:
		# 		reqData.append({'Request Accept':'False'})
		# 	if Customerobj.requestReject:
		# 		reqData.append({'Request Rejected':'True'})
		# 	else:
		# 		reqData.append({'Request Rejected':'False'})
		# 	if Customerobj.requestPaid:
		# 		reqData.append({'Request Paid':'True'})
		# 	else:
		# 		reqData.append({'Request Paid':'False'})
		# 	serializer = CustomerJobSerializer(Customerobj, many=True)
		# 	print(serializer.data)
		# 	return JsonResponse({ 'code': 200 ,'Request Status':reqData,'data' : serializer.data }, status=200, safe=False)

class sendParcelToTraveller(APIView):
	# permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		session_token_val = request.POST.get('session_token')
		
		main_user_obj=MainUser.objects.filter(token=session_token_val)
		print(main_user_obj)
		try:
			if main_user_obj:
				travellerId = request.POST.get('travllerId')
				if not travellerId:
					return Response({'status': 0, 'message': 'Traveller Id is Empty',})
				print(travellerId)
				supplierObj = SupplierJob.objects.filter(traveller_id=travellerId)
				if not supplierObj:
					return Response({'status': 0, 'message': 'No Supplier with this ID',})
				pickup_addr_val = request.POST.get('pickupAddress')
				# additional_addr_val = request.POST.get('additional_addr')

				country_nm_val = request.POST.get('fromCountry')
				if not country_nm_val:
					return Response({'status': 0, 'message': 'From Country Name Required',})



				city_nm_val = request.POST.get('fromCity')
				if not city_nm_val:
					return Response({'status': 0, 'message': 'From City Name Required',})
				postal_code_val = request.POST.get('postal_code')
				
				rec_name_val = request.POST.get('recName')
				if not rec_name_val:
					return Response({'status': 0, 'message': 'Recipient Name Required',})


				rec_countrycode_val = request.POST.get('countryCode')
				if not rec_countrycode_val:
					return Response({'status': 0, 'message': 'Recipient Country Code Required',})


				rec_phone_val = request.POST.get('recPhone')
				if not rec_phone_val:
					return Response({'status': 0, 'message': 'Recipient Phone Number Required',})


				parcel_drop_addr_val = request.POST.get('parcelDropAdrrs')
				if not parcel_drop_addr_val:
					return Response({'status': 0, 'message': 'Parcel Drop Address Required',})
				# rec_additional_addr_val = request.POST.get('rec_additional_addr')
				# rec_additional_addr_val = rec_additional_addr_val.encode('utf-8')
				rec_country_nm_val = request.POST.get('recCountry')
				if not rec_country_nm_val:
					return Response({'status': 0, 'message': 'Recipient Country Name Required',})

				rec_city_nm_val = request.POST.get('recCity')
				if not rec_city_nm_val:
					return Response({'status': 0, 'message': 'Recipient City Name Required',})


				parcel_wt_val = request.POST.get('parcelWeight')
				if not parcel_wt_val:
					return Response({'status': 0, 'message': 'Parcel Weight Required',})
				parcel_des_val = request.POST.get('parcelDesc')


				if not parcel_des_val:
					return Response({'status': 0, 'message': 'Parcel Description Required',})
				promocode_val = request.POST.get('promocode')

				last_customer_obj=CustomerJob.objects.last()
				if last_customer_obj is None:
					print("last travller id not find")
					new_traveller_id=str(10000+1)
				else:
				    latest_customer_id = int(last_customer_obj.parcel_id) #10267
				    print("last travleer is find")
				    new_customer_id = str(latest_customer_id+1)
				customer_obj=Customer.objects.filter(user=main_user_obj[0])
				if customer_obj:
					pass
				else:
					customer_obj=Customer.objects.create(user=main_user_obj[0])
					customer_obj=Customer.objects.filter(user=main_user_obj[0])
				print('2')
				try:
					CustomerJob.objects.create(travller=supplierObj[0].user,user=customer_obj[0],fromcountry=country_nm_val,fromcity=city_nm_val,receivername=rec_name_val,receivercountrycode=rec_countrycode_val,receiverphone=rec_phone_val,receiverdropaddress=parcel_drop_addr_val,tocountry=rec_country_nm_val,tocity=rec_city_nm_val,parcelweight=parcel_wt_val,description=parcel_des_val,requestSend=True,parcel_id=new_customer_id)
				except Exception as e:
					return Response({ 'status':500,'status':'false','message': str(e),})
				return Response({ 'status':200,'status':'true','message': 'Request Sent',})
					
			else:
				return Response({ 'status':500,'status':'false','message': 'User not logged in.',})
		except Exception as e:
			print(e)
			return Response({ 'status':500,'status':'false','message': str(e),})


@method_decorator(checklogin, name='dispatch')
class UpdateProfilePicture(APIView):
	def post(self, request, *args, **kwargs):
		print('UpdateProfile - in post')
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		try:
			print('data is  : ',request.FILES)
		except Exception as e:
			print('data is jj')
			pass
		session_token_val = request.POST.get('session_token')
		# otp_val = request.POST.get('otp')
		if not session_token_val:
			return Response({'code': 400,'status':'false','message': 'User not Logged In'})
		
		obj=MainUser.objects.filter(token=session_token_val)
		try:
			if obj:
				Extra_True=True
				# if((time>st_time) and (time<ex_time)):
				if Extra_True:
					from PIL import Image		
					image = request.FILES.get('image')
					if not image:
						return Response({'code': 400,'status':'false','message': 'Image Required for Update Profile picture'})
					if image:
						filename = image.name
						print('\n')
						print(filename)
						print('\n')
						filename = filename.split('.')
						extension = str(filename[-1])
						import io

						image_data = io.BytesIO(image.read())
						print('3')

						print(image_data)
						img = Image.open(image_data)
						# img.load()
						print('4')
						import random,string
						st = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
						thumbnailsize_objs = ThumbnailSize.objects.all()
						print('beforee resizing')
						for thumbnailsize in thumbnailsize_objs:
							print(thumbnailsize.height,thumbnailsize.width)
							img = Image.open(image_data)
							im = img.thumbnail([int(thumbnailsize.height),int(thumbnailsize.width)], Image.ANTIALIAS)
							# img = Image.resize([int(obj.height),int(obj.width)],PIL.Image.ANTIALIAS)
							im = img.save(str(settings.BASE_DIR)+'/media/'+str(thumbnailsize.height)+'*'+str(thumbnailsize.width)+'-'+st+'.'+extension)
							filename=str(settings.WEB_BASE_URL)+'media/'+str(thumbnailsize.height)+'*'+str(thumbnailsize.width)+'-'+st+'.'+extension

						img = Image.open(image_data)	
						img.save(str(settings.BASE_DIR)+'/media/original-'+st+'.'+extension)	
						# filename=st+'.'+extension
						# print(filename)
						# filename = str(settings.API_BASE_URL)+ 'media/original-'+str(st)+'.'+str(extension)
						# filename = str(settings.WEB_BASE_URL)+ 'media/original-'+str(st)+'.'+str(extension)
						# filename =
						print('filename = ',filename)

					if image:
						MainUser.objects.filter(token=session_token_val).update(image=filename)
					else:
						Response({'codec': 200, 'status':'true','status_message': 'Profile not updated'})

					main_user_obj = MainUser.objects.filter(token=session_token_val)
					main_user_obj_fcmtoken=main_user_obj[0].fcmtoken

					if '//' in main_user_obj[0].image.name:
						print('ful url exists')
						image = main_user_obj[0].image.name
					else:
						image = str(settings.WEB_BASE_URL)+'media/200*200-'+main_user_obj[0].image.name
					print("profile updated")

					return Response({'codec': 200, 'message': 'Profile updated successfully','image':image,'status':'true','status_message': 'Profile updated successfully'})					
			else:
				return Response({'status': 500, 'message': 'User Not Logged In'})
		except Exception as e:
			return Response({'status': 500, 'message': str(e)})


class TravelBy(APIView):
	# permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n')
		print('data is  : ',request.POST)
		try:
			obj=TravelByList.objects.all()
			if obj:
				serializer = TravelByListSeralizer(obj, many=True)
				print(serializer.data)
				return JsonResponse({ 'code': 200 , 'data' : serializer.data,'status':'true'}, status=200, safe=False)
			else:
				return Response({'code': 204, 'message': 'No vehical type found','status':'false'})	
		except Exception as e:	
			return Response({'code': 500, 'message': str(e),'status':'false'})

class GetCountry(APIView):
	# permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n')
		print('data is  : ',request.POST)
		try:
			obj=Countries.objects.all()
			if obj:
				serializer = CountrySeralizer(obj, many=True)
				print(serializer.data)
				return JsonResponse({ 'code': 200 , 'data' : serializer.data,'status':'true'}, status=200, safe=False)
			else:
				return Response({'code': 204, 'message': 'No countries found','status':'false'})	
		except Exception as e:	
			return Response({'code': 500, 'message': str(e),'status':'false'})

class GetCity(APIView):
	# permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n')
		print('data is  : ',request.POST)
		country_id_val = request.POST.get('country_id')
		print(country_id_val)
		if not country_id_val:
			return Response({'code': 400, 'message': 'Enter country name','status': 'false'})
		try:
			print('1')
			country_obj = Countries.objects.get(id=country_id_val)
			obj=Cities.objects.filter(country=country_obj)
			print('2')
			if obj:
				print('3')
				serializer = CitySeralizer(obj, many=True)
				print(serializer.data)
				return JsonResponse({ 'code': 200 , 'data' : serializer.data,'status': 'true' })
			else:
				return Response({'code': 402, 'meesage': 'No cities found','status': 'true'})	
		except Exception as e:
			return Response({'code': 500, 'message': str(e),'status': 'false'})

class SignUpOTP(APIView):
	@csrf_exempt
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		try:
			data=[]
			print('data is  : ',request.POST)
			token_val = request.POST.get('token')
			if not token_val:
				return Response({'code':400,'status': 'false', 'message': 'Token Empty'})
			if not token_val=='yt$-2@jc_(!!yy*j1pn9gjvfb8^pa!gSfkvu7juy6eet6xtd4k':
				return Response({'code': 400,'status':'false','message': 'Invalid token'})
			name_val = request.POST.get('name')
			if not name_val:
				return Response({'code': 400,'status':'false','message': 'Name Empty'})
			emailid = request.POST.get('email')
			if not emailid:
				return Response({'code': 400,'status':'false','message': 'Email Empty'})
			country_code_val = request.POST.get('country_code')
			if not country_code_val:
				return Response({'code': 400,'status':'false','message': 'country_code empty'})
			referral_code = request.POST.get('referral_code')
			if not referral_code:
				referral_code='NONE'
			if '+' not in country_code_val:
				country_code_val = '+' + country_code_val
			phone_val = request.POST.get('phone')
			print(type(phone_val))
			if not phone_val:
				return Response({'code': 400,'status':'false','message': 'Mobile number empty'})
			password_val = request.POST.get('password')
			if not password_val:
				return Response({'code': 400,'status':'false','message': 'Password empty'})

			phonenumbercheck_obj = MainUser.objects.filter(email=emailid)
			if phonenumbercheck_obj:
				return Response({'code': 409,'status':'false','message': 'Email already exists.'})
			phonenumbercheck_obj = MainUser.objects.filter(role__role = 'normaluser',countrycode=country_code_val,phone=phone_val,status = '1')
			if phonenumbercheck_obj:
				return Response({'code': 409,'status':'false','message': 'Mobile number already exists.'})
			a=[]
			main_user_obj = MainUser.objects.filter(phone=phone_val)
			a.append('1')
			if main_user_obj:
				a.append('2')
				if main_user_obj[0].status=='1':
					a.append('3')
					return Response({'code': 409,'status':'false','message': 'User exists.'})
				else:
					a.append('4')
					pass
				for m in main_user_obj:
					data.append({'phone':m.phone,
						'Email':m.email,
						'name':m.name})
			else:
				a.append('5')
				main_user_obj=MainUser.objects.create(phone=phone_val,email=emailid)
			a.append('6')
			if main_user_obj:
				OTP=GernateOTP()
				print("OTP of 5 digits:", OTP)
				
				start_time=datetime.datetime.now()
				expire_time=datetime.datetime.now()+timedelta(minutes=20)
				if password_val:
					new_password_val = handler.hash(password_val)
				main_user_obj=MainUser.objects.filter(phone=phone_val).update(name=name_val,password=new_password_val,referralcode=referral_code,countrycode=country_code_val,phone=phone_val,signupOTP=OTP,mobileOTP=OTP)
				# main_user_obj.update(signupOTP=OTP,starttime=start_time,expiretime=expire_time)
				print('3')
				return Response({'code': 200,'status':'true','message':'OTP Send on Your Mobile Number','OTP':OTP})
		except Exception as e:
			print(e)
			return Response({'code': 500, 'status':'false','message': str(e)})

class SignUp(APIView):
	@csrf_exempt
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		
		print('data is  : ',request.POST)
		phone_val = request.POST.get('phone')
		if not phone_val:
			return Response({'code': 400,'status':'false','message': 'Phone Empty'})
		otp_val = request.POST.get('otp')
		if not otp_val:
			return Response({'code': 400,'status':'false','message': 'OTP Empty'})
		fcmtoken_val = request.POST.get('fcmtoken')
		if not fcmtoken_val:
			return Response({'code': 400,'status':'false','message': 'fcmtoken_val Empty'})
		if not fcmtoken_val=='yt$-2@jc_(!!yy*j1pn9gjvfb8^pa!gSfkvu7juy6eet6xtd4k':
			return Response({'code': 400,'status':'false','message': 'Invalid token'})
		
		try:
			main_user_obj=MainUser.objects.filter(phone=phone_val,mobileOTP=otp_val)
			if main_user_obj:
				if main_user_obj[0].status=='0':
					token = str(binascii.b2a_hex(os.urandom(20)))
					token=token.strip('b')
					token=token.strip("'")
					userrole_obj = UserRole.objects.get(role='normaluser')
					main_user_obj.update(role=userrole_obj,status='1',token=token,fcmtoken=fcmtoken_val,mobile_verified=True)
					main_user_obj_fcmtoken=main_user_obj[0].fcmtoken
					print(main_user_obj_fcmtoken)
					return Response({'code': 200,'status':'true','message': 'User registered successfully','session_token':token})
				elif main_user_obj[0].status=='1':
					return Response({'code': 409,'status':'false','message': 'User is already registered.'})
			else:
				return Response({'code': 400, 'status':'false','message': 'Invalid OTP'})
		except Exception as e:
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})

class Login(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		token_val = str(request.POST.get('token'))
		print(token_val)
		phone_val = request.POST.get('phone')
		password_val = request.POST.get('password')
		fcmtoken_val = request.POST.get('fcmtoken')
		print("one")
		if not fcmtoken_val:
			return Response({'code': 400,'staus':'false','message': 'fcmtoken_val Empty'})
		if not phone_val:
			email_val = request.POST.get('email')
			if not email_val:
				return Response({'code': 400,'staus':'false','message': 'Email or Mobile is required'})
		print("two")
		if not password_val:
			return Response({'code': 400,'status':'false','message': 'Password is required'})
		print("three")
		if token_val=='None':
			return Response({'code': 400,'status':'false','message': 'Token Empty'})
		elif not token_val=='yt$-2@jc_(!!yy*j1pn9gjvfb8^pa!gSfkvu7juy6eet6xtd4k':
			return Response({'code': 400,'status':'false','message': 'Invalid token'})		
		else:
			if not phone_val:
				mainuser_obj = MainUser.objects.filter(email=email_val,role__role='normaluser')
			else:
				mainuser_obj = MainUser.objects.filter(phone=phone_val,role__role='normaluser')
			if not mainuser_obj:
				return Response({'status': 400, 'message': 'Please enter valid credentials'})
			if not phone_val:
				obj=MainUser.objects.filter(email=email_val,role__role='normaluser',status='1')
			else:
				obj=MainUser.objects.filter(phone=phone_val,role__role='normaluser',status='1')
			if obj:
				new_passw=obj[0].password
				check=handler.verify(password_val, new_passw)
				if check:
					print("Four")
					# just_for_fun=True
					# if just_for_fun:
					if obj[0].mobile_verified:
						token = str(binascii.b2a_hex(os.urandom(20)))
						token=token.strip('b')
						token=token.strip("'")
						print("Five")
						if not phone_val:
							MainUser.objects.filter(email=email_val).update(token=token,fcmtoken=fcmtoken_val)
							main_user_obj = MainUser.objects.filter(email=email_val).first()
						else:
							MainUser.objects.filter(phone=phone_val).update(token=token,fcmtoken=fcmtoken_val)
							main_user_obj = MainUser.objects.filter(phone=phone_val).first()
						print("six")
						profile = False
						if main_user_obj:
							if main_user_obj.addressline1 and main_user_obj.country and main_user_obj.state and main_user_obj.city and main_user_obj.postalcode and main_user_obj.dateofbirth:
								profile = True
							print("seven")
						print("eight")
						address = main_user_obj.addressline1
						data={}
						if not main_user_obj.image.name:
							image=''
						else:
							if '//' in main_user_obj.image.name:
								print('full url exists')
								image = main_user_obj.image.name
								image = image.replace('original','200*200')
							else:
								image = str(settings.WEB_BASE_URL)+'media/200*200-'+main_user_obj.image.name
						data={}
						print('2')
						if not main_user_obj.addressline1:
							addressline1=''
						else:	
							addressline1=main_user_obj.addressline1
						# print(addressline1)
							# addressline1=
						if not main_user_obj.addressline2:
							addressline2=''
						else:	
							addressline2=main_user_obj.addressline2
						if not main_user_obj.country:
							country=''
						else:	
							country=main_user_obj.country
						if not main_user_obj.state:
							state=''
						else:	
							state=main_user_obj.state

						if not main_user_obj.city:
							city=''
						else:	
							city=main_user_obj.city
						if not main_user_obj.postalcode:
							postalcode=''
						else:	
							postalcode=main_user_obj.postalcode
						if not main_user_obj.dateofbirth:
							dateofbirth=''
						else:	
							dateofbirth=main_user_obj.dateofbirth.strftime("%d/%m/%Y")

						if '++' in main_user_obj.countrycode:
							countrycode = main_user_obj.countrycode.replace('++','+')
						else:
							countrycode = main_user_obj.countrycode

						print('3')
						print(image)
						data.update({

									'name':main_user_obj.name,
									'session_token':token,
									'email':main_user_obj.email,
									'countrycode':countrycode,
									'phone':main_user_obj.phone,
									'addressline1':addressline1,
									'addressline2':addressline2,
									'country':country,
									'state':state,
									'city':city,
									'postalcode':postalcode,
									'dateofbirth':dateofbirth,
									'image':image,
								})
						return JsonResponse({ 'code': 200 ,'status':'true','data' : data,'message' : 'User Logged In'})

				else:
					return Response({'code': 400,'status':'false','message': 'Please enter valid credentials'})
			else:
				# return Response({'code': 0, 'message': 'Your account is not verified. Please check your email to verify your account.',})
				return Response({'code': 409,'status':'false','message': 'User does not exist.'})
	


class ForgotPassword(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		try:	
			phoneid = request.POST.get('phone')

			if not phoneid:
				return Response({'status': 400, 'message': 'Mobile is Required'})		

			main_user_obj=MainUser.objects.filter(phone=phoneid)
			if main_user_obj:
				OTP=GernateOTP()
				
				start_time=datetime.datetime.now()
				expire_time=datetime.datetime.now()+timedelta(minutes=20)
				main_user_obj.update(forgotpasswordOTP=OTP,starttime=start_time,expiretime=expire_time)
				print('3')
				return JsonResponse({'code': 200,'status':'true','message': 'OTP send on Your Mobile','OTP':OTP})
			else:
				return Response({'code': 400,'status':'false','message': 'Mobile number does not exist','phone':phoneid})
		except Exception as e:
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})

class ForgotPasswordCheckOTP(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('ForgotPasswordCheckOTP API - in post')
		print('data is  : ',request.POST)
		try:
			phone = request.POST.get('phone')
			if not phone:
				return Response({'code': 400,'status':'false','message': 'Mobile is required'})	
			otp = request.POST.get('otp')
			if not otp:
				return Response({'code':400,'status':'false','message': 'OTP is required'})
			
			print('before main_user_obj')
			main_user_obj = MainUser.objects.filter(phone=phone,forgotpasswordOTP=otp)
			print('after main_user_obj')
			if main_user_obj:
				return Response({'code': 200,'status':'true','otpverified': True,'message':'OTP verified'})
			else:
				return Response({'code': 500,'status':'false','otpverified': False,'message':'Please Enter a valid OTP'})
		except Exception as e:
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})


class UpdatePassword(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		try:
			phone = request.POST.get('phone')
			if not phone:
				return Response({'code': 400,'status':'false','message': 'Mobile is required'})	
			otp = request.POST.get('otp')
			if not otp:
				return Response({'code': 400,'status':'false','message': 'OTP is required'})
			password = request.POST.get('newpassword')
			if not password:
				return Response({'code': 400,'status':'false','message': 'New password is required'})	
			
			print('before main_user_obj')
			main_user_obj = MainUser.objects.filter(phone=phone,forgotpasswordOTP=otp)
			print('after main_user_obj')
			if main_user_obj:
				if main_user_obj[0].status=='2':
					print('2')
					return Response({'code': 409,'status':'false','message': 'User is disabled. Contact SuperAdmin.'})
				if main_user_obj[0].status=='0':
					print('0')
					return Response({'code': 409,'status':'false','message': 'User is not registered with us.'})
				if main_user_obj[0].status=='1':
					print('1')
					new_password_val = handler.hash(password)
					print(new_password_val)
					main_user_obj=MainUser.objects.filter(phone=phone)
					if main_user_obj:
						main_user_obj.update(password=new_password_val)
						return Response({'code': 200,'status':'true','message': 'Password updated successfully'})
					else:
						return Response({'code': 500,'status':'false','message': 'Password not updated'})
			else:
				return Response({'code': 400,'status':'false','message': 'Invalid OTP'})
		except Exception as e:
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})


class GetProfile(APIView):
	def get(self, request):
		
		print('\n\n\n\n')
		print('data is  : ',request.GET)
		print('1')
		try:
			session_token_val = request.GET.get('session_token')
			if not session_token_val:
				return Response({'code': 400,'status':'false','message': 'User not logged in'})
			obj=MainUser.objects.filter(token=session_token_val)
			
			if obj:
				if not obj[0].image.name:
					image=''
				else:
					
					if '//' in obj[0].image.name:
						print('full url exists')
						image = obj[0].image.name
						image = image.replace('original','200*200')
					else:
						image = str(settings.WEB_BASE_URL)+'/media/200*200-'+obj[0].image.name

				data={}
				print('2')
				if not obj[0].addressline1:
					addressline1=''
				else:	
					addressline1=obj[0].addressline1
				# print(addressline1)
					# addressline1=
				if not obj[0].addressline2:
					addressline2=''
				else:	
					addressline2=obj[0].addressline2
				if not obj[0].country:
					country=''
				else:	
					country=obj[0].country
				if not obj[0].state:
					state=''
				else:	
					state=obj[0].state

				if not obj[0].city:
					city=''
				else:	
					city=obj[0].city
				if not obj[0].postalcode:
					postalcode=''
				else:	
					postalcode=obj[0].postalcode
				if not obj[0].dateofbirth:
					dateofbirth=''
				else:	
					dateofbirth=obj[0].dateofbirth.strftime("%d/%m/%Y")

				if '++' in obj[0].countrycode:
					countrycode = obj[0].countrycode.replace('++','+')
				else:
					countrycode = obj[0].countrycode

				print('3')
				print(image)
				data.update({
							'name':obj[0].name,
							'email':obj[0].email,
							'countrycode':countrycode,
							'phone':obj[0].phone,
							'addressline1':addressline1,
							'addressline2':addressline2,
							'country':country,
							'state':state,
							'city':city,
							'postalcode':postalcode,
							'dateofbirth':dateofbirth,
							'image':image,
						})
				return JsonResponse({ 'code': 200 ,'status':'true','data' : data,'message' : 'success'})
			else:
				return JsonResponse({'code': 500,'status':'false','message': 'User not logged in.'})
		except Exception as e:
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})

@method_decorator(checklogin, name='dispatch')
class UpdateProfileOTP(APIView):
	# permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('UpdateProfileOTP - in post')
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		session_token_val = request.POST.get('session_token')
		phone = request.POST.get('phone')
		
		obj = MainUser.objects.filter(token=session_token_val)
		try:
			if obj:
				image = request.FILES.get('image')
				country_code_val = request.POST.get('country_code')
				if not country_code_val:
					return Response({'code': 400,'status':'false','message': 'Country code is required'})
				country_code_val = country_code_val.strip()
				if '+' not in country_code_val:
					country_code_val = '+' + country_code_val
				print(country_code_val)
				emailid = request.POST.get('email')
				if not emailid:
					emailid=''
				phone_val = request.POST.get('phone')
				if not phone_val:
					return Response({'code': 400,'status':'false', 'message': 'Mobile number is required'})
				phone_val = phone_val.strip()
				add1 = request.POST.get('add1')
				if not add1:
					return Response({'code': 400,'status':'false', 'message': 'Address line 1 is required'})
				add2 = request.POST.get('add2')
				# if not add2:
				# 	return Response({'code': 0, 'error': 'add2 Empty',})
				country = request.POST.get('country')
				if not country:
					return Response({'code': 400,'status':'false', 'message': 'Country is required'})
				state = request.POST.get('state')
				if not state:
					return Response({'code': 400,'status':'false', 'message': 'State is required'})
				city = request.POST.get('city')
				if not city:
					return Response({'code': 400,'status':'false', 'message': 'City is required'})
				postalcode = request.POST.get('postalcode')
				if not postalcode:
					return Response({'code': 400,'status':'false', 'message': 'Postal code is required'})
				dob_val = request.POST.get('dob')
				if not dob_val:
					return Response({'code': 400,'status':'false', 'message': 'Date of birth is required'})
				try:
					dob=parse(dob_val)
					# dob_val=dob_val.split('/')
					# dob=str(dob_val[2])+'-'+str(dob_val[0])+'-'+str(dob_val[1])
				except Exception as e:
					return Response({'code': 400,'status':'false', 'message': 'Date of birth format should be (mm/dd/yyyy)'})
				
				print(dob)
				
				print('111111')
				userphone = obj[0].countrycode+obj[0].phone
				usernewphone = country_code_val + phone_val
				print(userphone)
				print(usernewphone)
				digits = "0123456789"
				OTP = ""
				for i in range(5) : 
					OTP += digits[math.floor(random.random() * 10)]
				print("OTP of 5 digits:", OTP)
				start_time = datetime.datetime.now(pytz.timezone('UTC'))
				# print('in otp start time = ',start_time)

				expire_time = start_time + timedelta(minutes=30)
				if(userphone == usernewphone):
					obj.update(updateprofileOTP=OTP,updateprofileOTP_starttime=start_time,updateprofileOTP_expiretime=expire_time)
					print('3')
					return JsonResponse({'code': 200,'status':'true','otpon':'email', 'message': 'OTP sent successfully on your email','OTP':OTP})
				else:
					# sns = boto3.client('sns', region_name='us-east-1',aws_access_key_id=str(settings.AWS_ACCESS_KEY_ID),aws_secret_access_key= str(settings.AWS_SECRET_ACCESS_KEY))
					# obj.update(mobileOTP=OTP,updateprofileOTP_starttime=start_time,updateprofileOTP_expiretime=expire_time)
					try:
						# response = sns.publish(
						    # PhoneNumber=usernewphone,
						    # Message = 'Your Airdely Profile update OTP code is : '+OTP,    
						# )
						return Response({'code': 200,'status':'true','otpon':'mobile', 'message': 'OTP sent successfully on your mobile','OTP':OTP})
					except Exception as e:
						print('mobile otp send error=',e)
						return Response({'code': 400,'status':'false', 'error': 'Invalid phone number'})

			else:
				return Response({'code': 400,'status':'false', 'message': 'User not logged in.'})
		except Exception as e:
			print('in last exception')
			print(e)
			return Response({'code': 500,'status':'false', 'message': str(e)})

		
@method_decorator(checklogin, name='dispatch')
class UpdateProfile(APIView):
	def post(self, request, *args, **kwargs):
		print('UpdateProfile - in post')
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		try:
			print('data is  : ',request.FILES)
		except Exception as e:
			print('data is jj')
			pass
		session_token_val = request.POST.get('session_token')
		# otp_val = request.POST.get('otp')
		if not session_token_val:
			return Response({'code': 400,'status':'false','message': 'User not Logged In'})
		
		obj=MainUser.objects.filter(token=session_token_val)
		try:
			if obj:
				Extra_True=True
				# if((time>st_time) and (time<ex_time)):
				if Extra_True:
					from PIL import Image		
					image = request.FILES.get('image')
					
					if image:
						filename = image.name
						print('\n')
						print(filename)
						print('\n')
						filename = filename.split('.')
						extension = str(filename[-1])
						import io

						image_data = io.BytesIO(image.read())
						print('3')

						print(image_data)
						img = Image.open(image_data)
						# img.load()
						print('4')
						import random,string
						st = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
						thumbnailsize_objs = ThumbnailSize.objects.all()
						print('beforee resizing')
						for thumbnailsize in thumbnailsize_objs:
							print(thumbnailsize.height,thumbnailsize.width)
							img = Image.open(image_data)
							im = img.thumbnail([int(thumbnailsize.height),int(thumbnailsize.width)], Image.ANTIALIAS)
							# img = Image.resize([int(obj.height),int(obj.width)],PIL.Image.ANTIALIAS)
							im = img.save(str(settings.BASE_DIR)+'/media/'+str(thumbnailsize.height)+'*'+str(thumbnailsize.width)+'-'+st+'.'+extension)
							filename=str(settings.WEB_BASE_URL)+'media/'+str(thumbnailsize.height)+'*'+str(thumbnailsize.width)+'-'+st+'.'+extension

						img = Image.open(image_data)	
						img.save(str(settings.BASE_DIR)+'/media/original-'+st+'.'+extension)	
						# filename=st+'.'+extension
						# print(filename)
						# filename = str(settings.API_BASE_URL)+ 'media/original-'+str(st)+'.'+str(extension)
						# filename = str(settings.WEB_BASE_URL)+ 'media/original-'+str(st)+'.'+str(extension)
						# filename =
						print('filename = ',filename)

					username = request.POST.get('name')
					if not username:
						username=obj[0].name
					country_code_val = request.POST.get('country_code')
					if not country_code_val:
						country_code_val=obj[0].countrycode
						# return Response({'code': 400,'status':'false','message': 'Country code is required'})
					country_code_val = country_code_val.strip()
					if '+' not in country_code_val:
						country_code_val = '+' + country_code_val
					phone_val = request.POST.get('phone')
					if not phone_val:
						phone_val=obj[0].phone
						# return Response({'code': 400,'status':'false','message': 'Mobile number is required'})
					phone_val = phone_val.strip()
					add1 = request.POST.get('add1')
					if not add1:
						add1=obj[0].addressline1
						# return Response({'code': 400,'status':'false', 'message': 'Address line 1 is required'})
					add2 = request.POST.get('add2')
					country = request.POST.get('country')
					if not country:
						country=obj[0].country
						# return Response({'code': 400,'status':'false', 'message': 'Country is required'})
					if obj[0].country:
						if obj[0].country == country:
							pass
					state = request.POST.get('state')
					if not state:
						state=obj[0].state
						# return Response({'code': 400,'status':'false','message': 'State is required'})
					city = request.POST.get('city')
					if not city:
						city=obj[0].city
						# return Response({'status': 0, 'message': 'City is required','status_code': 0, 'status_message': 'City is required'})
					postalcode = request.POST.get('postalcode')
					if not postalcode:
						postalcode=obj[0].postalcode
						# return Response({'status': 0, 'message': 'Postal code is required','status_code': 0, 'status_message': 'Postal code is required'})
					dob_val = request.POST.get('dob')
					if not dob_val:
						dob=obj[0].dateofbirth
						# return Response({'status': 0, 'message': 'Date of birth is required','status_code': 0, 'status_message': 'Date of birth is required'})
					else:
						try:
							dob_val = dob_val.split('-')
							dob_val = str(dob_val[1])+'/'+str(dob_val[2])+'/'+str(dob_val[0])
							dob = parse(dob_val)
						except:
							return Response({'status': 0, 'message': 'Date of birth format should be (mm/dd/yyyy)','status_code': 0, 'status_message': 'Date of birth format should be (mm/dd/yyyy)'})
					
					# print(dob)
					if image:
						MainUser.objects.filter(token=session_token_val).update(name=username,image=filename,countrycode=country_code_val,phone=phone_val,addressline1=add1,addressline2=add2,country=country,state=state,city=city,postalcode=postalcode,dateofbirth=dob)
					else:
						MainUser.objects.filter(token=session_token_val).update(name=username,countrycode=country_code_val,phone=phone_val,addressline1=add1,addressline2=add2,country=country,state=state,city=city,postalcode=postalcode,dateofbirth=dob)
					
					main_user_obj = MainUser.objects.filter(token=session_token_val)
					main_user_obj_fcmtoken=main_user_obj[0].fcmtoken

					if '//' in main_user_obj[0].image.name:
						print('ful url exists')
						image = main_user_obj[0].image.name
					else:
						image = str(settings.WEB_BASE_URL)+'media/200*200-'+main_user_obj[0].image.name
					print("profile updated")
					obj_for_user=MainUser.objects.filter(token=session_token_val)
					data={}
					print('2')
					main_user_obj=obj_for_user[0]
					if main_user_obj:
						if not main_user_obj.addressline1:
							addressline1=''
						else:	
							addressline1=main_user_obj.addressline1
						# print(addressline1)
							# addressline1=
						if not main_user_obj.addressline2:
							addressline2=''
						else:	
							addressline2=main_user_obj.addressline2
						if not main_user_obj.country:
							country=''
						else:	
							country=main_user_obj.country
						if not main_user_obj.state:
							state=''
						else:	
							state=main_user_obj.state

						if not main_user_obj.city:
							city=''
						else:	
							city=main_user_obj.city
						if not main_user_obj.postalcode:
							postalcode=''
						else:	
							postalcode=main_user_obj.postalcode
						if not main_user_obj.dateofbirth:
							dateofbirth=''
						else:	
							dateofbirth=main_user_obj.dateofbirth.strftime("%d/%m/%Y")

						if '++' in main_user_obj.countrycode:
							countrycode = main_user_obj.countrycode.replace('++','+')
						else:
							countrycode = main_user_obj.countrycode

						print('3')
						print(image)
						data.update({

									'name':main_user_obj.name,
									# 'session_token':token,
									'email':main_user_obj.email,
									'countrycode':countrycode,
									'phone':main_user_obj.phone,
									'addressline1':addressline1,
									'addressline2':addressline2,
									'country':country,
									'state':state,
									'city':city,
									'postalcode':postalcode,
									'dateofbirth':dateofbirth,
									'image':image,
								})
					else:
						return Response({'codec': 200, 'message': 'Profile updated successfully','image':image,'status':'true','status_message': 'Profile updated successfully'})
					return Response({'codec': 200, 'message': 'Profile updated successfully','data':data,'status':'true','status_message': 'Profile updated successfully'})					
			else:
				return Response({'status': 500, 'message': 'User Not Logged In'})
		except Exception as e:
			return Response({'status': 500, 'message': str(e)})

@method_decorator(checklogin, name='dispatch')
class RegisterTraveller(APIView):
	def post(self, request, *args, **kwargs):
		try:
			print('RegisterTraveller - in post')
			print(request.POST)
			session_token_val = request.POST.get('session_token')
			from_country_nm = request.POST.get('from_country_nm')
			if not from_country_nm:
				return Response({'code': 400,'status':'false','message': 'Enter from_country_nm'})
			print(from_country_nm)
			from_city_nm = request.POST.get('from_city_nm')
			if not from_city_nm:
				return Response({'code': 400,'status':'false','message': 'Enter from_city_nm'})
			print(from_city_nm)
			# print(dep_airport)
			dep_date = request.POST.get('dep_date')
			if not dep_date:
				return Response({'code': 400,'status':'false','message': 'Enter dep_date'})
			print("fine here")
			# dep_date=parse(dep_date)
			dep_date = dep_date.split('-')
			print(dep_date[1])
			print(dep_date[0])
			print(dep_date[2])
			dep_date = str(dep_date[1])+'/'+str(dep_date[2])+'/'+str(dep_date[0])
			dep_date = parse(dep_date)
			print("fine two")
			print(dep_date)
			dep_time = request.POST.get('dep_time')
			if not dep_time:
				return Response({'code': 400,'status':'false','message': 'Enter dep_time'})

			dep_time = parse(dep_time).time()
			print(dep_time)

			departuredatetime = datetime.datetime.combine(dep_date.date(),dep_time)
			print('\n\n\n\n\n\n')
			print('departuredatetime = ',departuredatetime)
			print('\n\n\n\n\n\n')


			to_country_nm = request.POST.get('to_country_nm')
			if not to_country_nm:
				return Response({'code': 400,'status':'false','message': 'Enter to_country_nm'})
			print(to_country_nm)

			if to_country_nm==from_country_nm:
				return Response({'code': 400,'status':'false','message': 'Destination Country must be different from Boarding Country.'})
			to_city_nm = request.POST.get('to_city_nm')
			if not to_city_nm:
				return Response({'code': 400,'status':'false','message':'Enter to_city_nm'})
			print(to_city_nm)
			arrival_date = request.POST.get('arrival_date')
			if not arrival_date:
				return Response({'code': 400,'status':'false','message': 'Enter arrival_date'})
			arrival_date = arrival_date.split('-')
			arrival_date = str(arrival_date[1])+'/'+str(arrival_date[2])+'/'+str(arrival_date[0])
			arrival_date = parse(arrival_date)

			print(arrival_date)
			arrival_time = request.POST.get('arrival_time')
			if not arrival_time:
				return Response({'code': 400,'status':'false','message': 'Enter arrival_time'})
			arrival_time = parse(arrival_time).time()
			print(arrival_time)

			arrivaldatetime = datetime.datetime.combine(arrival_date.date(),arrival_time)
			print('\n\n\n\n\n\n')
			print('arrivaldatetime = ',arrivaldatetime)
			print('\n\n\n\n\n\n')

			print('\n\n\n\n\n\n')
			print('departuredatetime = ',departuredatetime)
			print('arrivaldatetime = ',arrivaldatetime)
			print('\n\n\n\n\n\n')

			per_kg_charges = request.POST.get('charges')
			# unused_luggage = u
			# unused_luggage = unicode(unused_luggage, "utf-8")
			if not per_kg_charges:
				return Response({'code': 400, 'status':'false','message': 'Please Enter Per KG charges'})
			print(per_kg_charges)

			travelled_by = request.POST.get('travel_by')
			if not travelled_by:
				return Response({'code': 400,'status':'false','message': 'Enter Travell By'})
			

			main_usr_obj=MainUser.objects.filter(token=session_token_val)
			print(main_usr_obj)
			last_supplierjob_obj=SupplierJob.objects.last()
			print(last_supplierjob_obj)
			if last_supplierjob_obj is None:
				print("last travller id not find")
				new_traveller_id=str(10000+1)
			else:
			    latest_traveller_id = int(last_supplierjob_obj.traveller_id) #10267
			    print("last travleer is find")
			    new_traveller_id = str(latest_traveller_id+1)
				

			s =[char for char in new_traveller_id]
			s[0]=str(s[0])+'0'
			s=''.join(s) #100267
			new_atn_number='ATN-'+from_country_nm+'-'+to_country_nm+'-'+s


			if main_usr_obj:
				supplier_obj=Supplier.objects.filter(user=main_usr_obj[0])
				if supplier_obj:
					supplier_job_obj = SupplierJob.objects.create(user=supplier_obj[0],traveller_id=new_traveller_id,atnnumber= new_atn_number,fromcountry=from_country_nm,fromcity=from_city_nm,departuredate=dep_date,departuretime=dep_time,tocountry=to_country_nm,tocity=to_city_nm,arrivaldate=arrival_date,arrivaltime=arrival_time,travel_by=travelled_by,chrgesperkg=int(per_kg_charges))	
				else:
					supplier_obj=Supplier.objects.create(user=main_usr_obj[0])
					supplier_job_obj = SupplierJob.objects.create(user=supplier_obj,traveller_id=new_traveller_id,atnnumber= new_atn_number,fromcountry=from_country_nm,fromcity=from_city_nm,departuredate=dep_date,departuretime=dep_time,tocountry=to_country_nm,tocity=to_city_nm,arrivaldate=arrival_date,arrivaltime=arrival_time,travel_by=travelled_by,chrgesperkg=int(per_kg_charges))
				print('\n\n\n\n  111 \n\n\n\n')

				supplierjob_obj = SupplierJob.objects.last()
			
				# return Response({'code': 200,'status':'true','message': 'Your travelling details are successfully registered.','atn_filepath':atn_filepath})
				return Response({'code': 200,'status':'true','message': 'Your travelling details are successfully registered.'})
			else:
				return Response({'code': 400,'status':'false','message': 'User not logged in.'})
		except Exception as e:
			print('in exception')
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})



class searchTravller(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		try:
			print("one")
			country = request.POST.get('fromCountry')
			if not country:
				return Response({'code': 400,'status':'false','message': 'Country is required'})	
			des_country = request.POST.get('toCountry')
			if not des_country:
				return Response({'code': 400,'status':'false','message': 'Destination Country is required'})
			des_city = request.POST.get('toCity')
			print("two")
			if not des_city:
				return Response({'code': 400,'status':'false','message': 'Destination City is required'})	
			city = request.POST.get('fromCity')
			print("two")
			if not city:
				return Response({'code': 400,'status':'false','message': 'City is required'})
			start_date = request.POST.get('searchDate')
			print("three")
			if not start_date:
				return Response({'code': 400,'status':'false','message': 'Date is required'})
			time = request.POST.get('searchTime')
			print("three")
			if not time:
				return Response({'code': 400,'status':'false','message': 'Time is required'})
			print("four")	
			start_date = start_date.split('-')
			start_date = str(start_date[1])+'/'+str(start_date[2])+'/'+str(start_date[0])
			start_date = parse(start_date)
			print("five")
			print('before main_user_obj')
			print("==================here from enterd date")
			dep_time = parse(time).time()
			print(dep_time)

			departuredatetime = datetime.datetime.combine(start_date.date(),dep_time)
			print(type(departuredatetime))
			print(departuredatetime)
			main_user_obj = SupplierJob.objects.filter(Q(fromcountry=country)&Q(tocountry=des_country)&Q(tocity=des_city)&Q(fromcity=city))
			# print('after main_user_obj')
			# print("six")
			print(main_user_obj)
			timeuser='not'
			print("==================here from new date")
			alluser=[]
			for user in main_user_obj:
				print(type(user.departuretime))
				new_time = user.departuretime
				print(new_time)
				newdate=user.departuredate
				newdeparturedatetime = datetime.datetime.combine(newdate,new_time)
				print(type(newdeparturedatetime))
				print(newdeparturedatetime)
				if(newdeparturedatetime>=departuredatetime):
					image=''
					if not user.user.user.image.name:
						image=''
					else:
						if '//' in user.user.user.image.name:
							print('full url exists')
							image = user.user.user.image.name
							image = image.replace('original','200*200')
						else:
							image = str(settings.WEB_BASE_URL)+'media/200*200-'+user.user.user.image.name
					alluser.append({'ID':user.traveller_id,
						             'Name':user.user.user.name,
						             'Phone':user.user.user.phone,
						             'Departure Time':user.departuretime,
						             'Arrival Time':user.arrivaltime,
						             'Rating':2,
						             'Completed Task':0,
						             'Profile Picture':image,
						             'Charges per KG':user.chrgesperkg,
						             'From Country':user.fromcountry,
						             'From City':user.fromcity,
						             'Departure Date':user.departuredate,
						             'To country':user.tocountry,
						             'To city':user.tocity,
						             'Arrival Date':user.arrivaldate,
						             'Travel By':user.travel_by
						           })
			print(alluser)
			if main_user_obj:
				return Response({'code': 200,'status':'true','message': 'Travller Find','List':alluser})
			else:
				print("seven")
				return Response({'code': 200,'status':'true','message': 'Travller Not Find','List':alluser})
		except Exception as e:
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})


class searchTravllerByid(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n\n\n')
		print('data is  : ',request.POST)
		try:
			print("one")
			traveller_id = request.POST.get('id')
			if not traveller_id:
				return Response({'code': 400,'status':'false','message': 'Travller id is required'})	
			# print(departuredatetime)
			main_user_obj = SupplierJob.objects.filter(Q(traveller_id=traveller_id))
			print(main_user_obj[0])
			try:
				print(main_user_obj[0].user.user.name)
			except Exception as e:
				print(e)
			if main_user_obj:
				return Response({'code': 200,'status':'true','message': 'Travller Find','Travller Name':main_user_obj[0].user.user.name,'Travller Phone':main_user_obj[0].user.user.phone,'From Country':main_user_obj[0].fromcountry,'From City':main_user_obj[0].fromcity,'To Country':main_user_obj[0].tocountry,'To City':main_user_obj[0].tocity,'Departure Date':main_user_obj[0].departuredate,'Departure Time':main_user_obj[0].departuretime,'Arrival Date':main_user_obj[0].arrivaldate,'Arrival Time':main_user_obj[0].arrivaltime,'Travlled By':'Car'})
			else:
				print("seven")
				return Response({'code': 200,'status':'true','message': 'Travller Not Find'})
		except Exception as e:
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})


def GernateOTP():
	digits = "0123456789"
	OTP = ""
	for i in range(5) :
		OTP += digits[math.floor(random.random() * 10)]
	return OTP



class DeleteTravel(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n')
		print('ShowTravellerDetailsToTravellerTest API - in post')
		print('data is  : ',request.POST)
		a=[]
		try:
			session = request.POST.get('session_token')
			if not session:
				return Response({'code': 400, 'status': 'false','message':'User Not Logged IN'})
			travel_id = request.POST.get('travel_id')
			if not travel_id:
				return Response({'code': 400, 'status': 'false','message':'Traveller ID is Required'})
			main_obj_get=MainUser.objects.filter(token=session)
			if not main_obj_get:
				return Response({'code': 400, 'status': 'false','message':'User not Logged IN'})
			supplier_obj=Supplier.objects.filter(user=main_obj_get[0])
			if not supplier_obj:
				return Response({'code': 400, 'status': 'false','message':'You are not register as Travller'})
			data_send=[]
			supplier_job_obj=SupplierJob.objects.filter(user=supplier_obj[0],traveller_id=travel_id)
			if supplier_job_obj:
				try:
					supplier_job_obj[0].delete()
				except Exception as e:
					return Response({'code': 500, 'status': 'false','message':str(e)})
			else:
				return Response({'code': 400, 'status': 'false','message':'Not find any Traveling Details'})
			return Response({'code': 200, 'status': 'true','message':'Traveling record deleted successfully'})
		except Exception as e:
			return Response({'code': 500, 'status': 'false','message':str(e)})

@method_decorator(checklogin, name='dispatch')
class UpdateTravel(APIView):
	def post(self, request, *args, **kwargs):
		try:
			print('RegisterTraveller - in post')
			print(request.POST)
			session_token_val = request.POST.get('session_token')
			if not session_token_val:
				return Response({'code': 400,'status':'false','message': 'Session Token is required'})
			travel_id = request.POST.get('travel_id')
			if not travel_id:
				return Response({'code': 400,'status':'false','message': 'Travelling Details not Found,Travelling id in required'})
			main_usr_obj=MainUser.objects.filter(token=session_token_val)
			if main_usr_obj:
				supplier_obj=Supplier.objects.filter(user=main_usr_obj[0])
				if supplier_obj:
					supplier_job_obj = SupplierJob.objects.filter(user=supplier_obj[0],traveller_id=travel_id)
					supplier_job_obj=supplier_job_obj[0]
				else:
					return Response({'code': 400,'status':'false','message': 'User Not Logged In'})
				if not supplier_job_obj:
					return Response({'code': 400,'status':'false','message': 'User Not Logged In'})
					
				
				from_country_nm = request.POST.get('from_country_nm')
				if not from_country_nm:
					from_country_nm=supplier_job_obj.fromcountry

				from_city_nm = request.POST.get('from_city_nm')
				if not from_city_nm:
					from_city_nm=supplier_job_obj.fromcity
				# dep_airport='NIL'
				dep_date = request.POST.get('dep_date')
				if not dep_date:
					dep_date=supplier_job_obj.departuredate
				else:
					# dep_date=parse(dep_date)
					dep_date = dep_date.split('-')
					print(dep_date[1])
					print(dep_date[0])
					print(dep_date[2])
					dep_date = str(dep_date[1])+'/'+str(dep_date[2])+'/'+str(dep_date[0])
					dep_date = parse(dep_date)
					print("fine two")
					print(dep_date)

				dep_time = request.POST.get('dep_time')
				if not dep_time:
					dep_time=supplier_job_obj.departuretime
				else:
					dep_time = parse(dep_time).time()
					print(dep_time)

					departuredatetime = datetime.datetime.combine(dep_date.date(),dep_time)
					print('\n\n\n\n\n\n')
					print('departuredatetime = ',departuredatetime)
					print('\n\n\n\n\n\n')

				to_country_nm = request.POST.get('to_country_nm')
				if not to_country_nm:
					to_country_nm=supplier_job_obj.tocountry

				# if to_country_nm==from_country_nm:
					# return Response({'code': 400,'status':'false','message': 'Destination Country must be different from Boarding Country.'})
				to_city_nm = request.POST.get('to_city_nm')
				if not to_city_nm:
					to_city_nm=supplier_job_obj.tocity
					# return Response({'code': 400,'status':'false','message':'Enter to_city_nm'})
				print(to_city_nm)

				# des_airport ='NIL'
				arrival_date = request.POST.get('arrival_date')
				if not arrival_date:
					arrival_date=supplier_job_obj.arrivaldate
				else:
					arrival_date = arrival_date.split('-')
					arrival_date = str(arrival_date[1])+'/'+str(arrival_date[2])+'/'+str(arrival_date[0])
					arrival_date = parse(arrival_date)
					print(arrival_date)

				arrival_time = request.POST.get('arrival_time')
				if not arrival_time:
					arrival_time=supplier_job_obj.arrivaltime
				else:	
					arrival_time = parse(arrival_time).time()
					print(arrival_time)

					arrivaldatetime = datetime.datetime.combine(arrival_date.date(),arrival_time)
					print('\n\n\n\n\n\n')
					print('arrivaldatetime = ',arrivaldatetime)
					print('\n\n\n\n\n\n')

					print('\n\n\n\n\n\n')
					print('departuredatetime = ',departuredatetime)
					print('arrivaldatetime = ',arrivaldatetime)
					print('\n\n\n\n\n\n')

				per_kg_charges = request.POST.get('charges')
				# unused_luggage = u
				# unused_luggage = unicode(unused_luggage, "utf-8")
				if not per_kg_charges:
					per_kg_charges=supplier_job_obj.chrgesperkg
					# return Response({'code': 400, 'status':'false','message': 'Enter unused_luggage'})
				print(per_kg_charges)

				travelled_by = request.POST.get('travel_by')
				if not travelled_by:
					travelled_by=supplier_job_obj.travel_by
					# return Response({'code': 400,'status':'false','message': 'Enter Travell By'})

				s =[char for char in travel_id]
				s[0]=str(s[0])+'0'
				s=''.join(s) #100267
				new_atn_number='ATN-'+from_country_nm+'-'+to_country_nm+'-'+s
				SupplierJob.objects.filter(user=supplier_obj[0],traveller_id=travel_id).update(atnnumber= new_atn_number,fromcountry=from_country_nm,fromcity=from_city_nm,departuredate=dep_date,departuretime=dep_time,tocountry=to_country_nm,tocity=to_city_nm,arrivaldate=arrival_date,arrivaltime=arrival_time,travel_by=travelled_by,chrgesperkg=int(per_kg_charges))	
				supplier_obj_after_update = SupplierJob.objects.filter(user=supplier_obj[0],traveller_id=travel_id)
				supplier_obj_after_update=supplier_obj_after_update[0]
				data=[]
				data.append({
					'FromCountry':supplier_obj_after_update.fromcountry,
					'From City':supplier_obj_after_update.fromcity,
					'Dep Date':supplier_obj_after_update.departuredate,
					'Dep Time':supplier_obj_after_update.departuretime,
					'To Country':supplier_obj_after_update.tocountry,
					'From Country':supplier_obj_after_update.tocity,
					'Arrival Date':supplier_obj_after_update.arrivaldate,
					'Arrival Time':supplier_obj_after_update.arrivaltime,
					'Charges':supplier_obj_after_update.chrgesperkg,
					'Travel By':supplier_obj_after_update.travel_by
					})

				return Response({'code': 200,'status':'true','message': 'Details Updated','data':data})
				# main_usr_obj=MainUser.objects.filter(token=session_token_val)
				# print(main_usr_obj)
				# last_supplierjob_obj=SupplierJob.objects.last()
				# print(last_supplierjob_obj)
				# if last_supplierjob_obj is None:
					# print("last travller id not find")
					# new_traveller_id=str(10000+1)
				# else:
				    # latest_traveller_id = int(last_supplierjob_obj.traveller_id) #10267
				    # print("last travleer is find")
				    # new_traveller_id = str(latest_traveller_id+1)
					

				# s =[char for char in new_traveller_id]
				# s[0]=str(s[0])+'0'
				# s=''.join(s) #100267
				# new_atn_number='ATN-'+from_country_nm+'-'+to_country_nm+'-'+s


			else:
				return Response({'code': 400,'status':'false','message': 'User Not Logged In'})
			


			# if main_usr_obj:
			# 	supplier_obj=Supplier.objects.filter(user=main_usr_obj[0])
			# 	supplier_job_obj = SupplierJob.objects.filter(user=supplier_obj[0],traveller_id=new_traveller_id)
			# 	if supplier_obj:
			# 		supplier_job_obj = SupplierJob.objects.create(user=supplier_obj[0],traveller_id=new_traveller_id,atnnumber= new_atn_number,fromcountry=from_country_nm,fromcity=from_city_nm,departuredate=dep_date,departuretime=dep_time,tocountry=to_country_nm,tocity=to_city_nm,destinationairport=des_airport,arrivaldate=arrival_date,arrivaltime=arrival_time,unusedluggage=unused_luggage, leftunusedluggage = leftunusedluggage, flightno=flight_no,ticketno=ticket_no,travel_by=travelled_by)	
			# 	else:
			# 		supplier_obj=Supplier.objects.create(user=main_usr_obj[0])
			# 		supplier_job_obj = SupplierJob.objects.create(user=supplier_obj,traveller_id=new_traveller_id,atnnumber= new_atn_number,fromcountry=from_country_nm,fromcity=from_city_nm,departuredate=dep_date,departuretime=dep_time,tocountry=to_country_nm,tocity=to_city_nm,destinationairport=des_airport,arrivaldate=arrival_date,arrivaltime=arrival_time,unusedluggage=unused_luggage, leftunusedluggage = leftunusedluggage, flightno=flight_no,ticketno=ticket_no,travel_by=travelled_by)
			# 	print('\n\n\n\n  111 \n\n\n\n')

			# 	supplierjob_obj = SupplierJob.objects.last()
			
			# 	# return Response({'code': 200,'status':'true','message': 'Your travelling details are successfully registered.','atn_filepath':atn_filepath})
			# 	return Response({'code': 200,'status':'true','message': 'Your travelling details are successfully registered.'})
			# else:
			# 	return Response({'code': 400,'status':'false','message': 'User not logged in.'})
		except Exception as e:
			print('in exception')
			print(e)
			return Response({'code': 500,'status':'false','message': str(e)})


class ShowTravellerDetailsToTravellerTest(APIView):
	# permission_classes = (IsAuthenticated,)
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		print('\n\n')
		print('ShowTravellerDetailsToTravellerTest API - in post')
		print('data is  : ',request.POST)
		a=[]
		try:
			session = request.POST.get('session_token')
			if not session:
				return Response({'code': 400, 'status': 'true'})
			a.append('1')
			# if notificationid_val:
			# 	notificationid_val = int(notificationid_val)
			# 	notification_obj = Notifications.objects.filter(id = notificationid_val).update(status='read')
			main_obj_get=MainUser.objects.filter(token=session)
			a.append('2')
			# traveller_id_val = request.POST.get('traveller_id')
			# if not traveller_id_val:
			# 	return Response({'code': 0, 'error': 'traveller_id_val Empty',})		
			# notification_obj = Notifications.objects.filter(id = notificationid_val).first()
			# if notification_obj:
			# 	awbnumber = notification_obj.relatedawbnumber
			# 	customerjob_obj = CustomerJob.objects.filter(awdnumber = awbnumber).first()
			supplier_obj=Supplier.objects.filter(user=main_obj_get[0])
			data_send=[]
			a.append('3')
			supplier_job_obj=SupplierJob.objects.filter(user=supplier_obj[0])
			a.append('4')
			for travel in supplier_job_obj:
				data_send.append({
					'id':travel.traveller_id,
					'From Country':travel.fromcountry,
					'From City':travel.fromcity,
					'To Country':travel.tocountry,
					'To city':travel.tocity,
					'Dep Date':travel.departuredate,
					'Dep Time':travel.departuretime,
					'Arrival Date':travel.arrivaldate,
					'Arrival Time':travel.arrivaltime,
					'per Kg Charges':travel.chrgesperkg,
					'Travel By':travel.travel_by,
					})
			a.append('5')
			return Response({'code': 200, 'data': data_send,'status':'true'})
		except Exception as e:
			return Response({'code': 0, 'error': str(e),})


# This code is only for Testing Purpose
def sendOTPmail(OTP,emailid,subject):
	port = 465  # For starttls
	smtp_server = "smtp.gmail.com"
	sender_email = "manii.6264s@gmail.com"
	receiver_email = emailid
	password = "mypassword"
	print(subject)
	message = MIMEMultipart("alternative")
	message["Subject"] = subject
	message["From"] = 'manii.6264s@gmail.com'
	message["To"] = emailid
	html="<h1>Hello,Welcome To our site</h1>"
	part2 = MIMEText(html, "html")
	message.attach(part2)
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		print(type(server))
		aa=server.login(sender_email, password)
		server.sendmail("manii.6264s@gmail.com", emailid, message.as_string())
		print("Email has been sent succesfully")
	except Exception as e:
		print(e)
	finally:
		server.quit() 	


