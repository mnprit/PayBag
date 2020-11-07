from django.conf.urls import url
from .views import *
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^signupotp$', SignUpOTP.as_view(), name='homepage'),# done
	url(r'^signup$', SignUp.as_view(), name='homepage'),# done

	url(r'^login$', Login.as_view(), name='homepage'), # done
	url(r'^forgotpassword$', ForgotPassword.as_view(), name='homepage'),
	# url(r'^checkotp$', CheckOTP.as_view(), name='homepage'),
	url(r'^forgotpasswordcheckotp$', ForgotPasswordCheckOTP.as_view(), name='homepage'), #18-12-2019
	url(r'^updatepassword$', UpdatePassword.as_view(), name='homepage'),
	url(r'^getprofile$', GetProfile.as_view(), name='homepage'), #done
	url(r'^updateprofileotp$', UpdateProfileOTP.as_view(), name='homepage'), #done
	url(r'^updateprofile$', UpdateProfile.as_view(), name='homepage'), #done
	url(r'^supplier/registertraveller', RegisterTraveller.as_view(), name='homepage'),
	url(r'^searchTravller$', searchTravller.as_view(), name='homepage'),# done
	url(r'^searchTravllerByid$', searchTravllerByid.as_view(), name='homepage'),
	url(r'^deletetravel', DeleteTravel.as_view(), name='homepage'), 
	url(r'^getcity$', GetCity.as_view(), name='homepage'), # shayad for delete 27-12-2019
	url(r'^getcountries$', GetCountry.as_view(), name='homepage'),
	url(r'^getTravelBy$', TravelBy.as_view(), name='homepage'),
	url(r'^updateTravel', UpdateTravel.as_view(), name='homepage'), 
	url(r'^updateProfilePicture', UpdateProfilePicture.as_view(), name='homepage'), 
	url(r'^showtravellerdetailstotraveller', ShowTravellerDetailsToTravellerTest.as_view(), name='homepage'),
	url(r'^sendParcel', sendParcelToTraveller.as_view(), name='homepage'),
	url(r'^notificationTravellerAndCustomer', notificationTravellerAndCustomer.as_view(), name='homepage'),
	url(r'^showAllParcelRequestsCustomer', ShowAllRequestsToCustomer.as_view(), name='homepage'),
	url(r'^acceptParcelRequest', AcceptParcelRequest.as_view(), name='homepage'),
	url(r'^rejectParcelRequest', RejectParcelRequest.as_view(), name='homepage'),
	url(r'^deleteParcelRequest', DeleteParcelRequest.as_view(), name='homepage'),
	url(r'^filterTraveller', filterTraveller.as_view(), name='homepage'),
	

	
	
]
