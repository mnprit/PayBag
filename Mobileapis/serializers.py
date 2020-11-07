from rest_framework import serializers
from Customer.models import CustomerJob




    # facilityid = models.CharField(max_length=20,null=True,blank=True)
    # image = models.FileField(null=True,blank=True,)
    # collectioncentrename = models.CharField(max_length=100,blank=True,null=True)
    # address = models.CharField(max_length=100,blank=True,null=True)
    # # country = models.CharField(max_length=100,blank=True,null=True)
    # country=models.ForeignKey(Countries,on_delete=models.CASCADE,null=True,blank=True)
    # city=models.ForeignKey(Cities,on_delete=models.CASCADE,null=True,blank=True)
    # airport=models.ForeignKey(Airports,on_delete=models.CASCADE,null=True,blank=True)
    
    # airdelycentre = models.BooleanField(default=False)
    # lastmiledeliverycentre = models.BooleanField(default=False)

    # openingtime = models.TimeField(max_length=100,null=True)
    # closingtime = models.TimeField(max_length=100,null=True)

    # startedfrom = models.DateField(default=datetime.datetime.now)
    # # operationalhours = models.CharField(max_length=100,blank=True,null=True)
    # status = models.CharField(max_length=100,blank=True,null=True) # status='1' for active & '0' for inactive




# class AirdelyFacilitiesSerializer(serializers.Serializer):
#     facilityid = serializers.CharField(max_length=100)
#     image = serializers.FileField(required=False)

#     collectioncentrename = serializers.CharField(max_length=100)
#     address = serializers.CharField(max_length=100)
#     country = serializers.ReadOnlyField(source='country.name')
#     city = serializers.ReadOnlyField(source='country.name')
#     airport = serializers.ReadOnlyField(source='country.name')
#     airdelycentre = serializers.BooleanField(required=False)
#     lastmiledeliverycentre = serializers.BooleanField(required=False)
#     openingtime = serializers.TimeField(required=False)
#     closingtime = serializers.TimeField(required=False)
#     startedfrom = serializers.DateField(required=False)
#     status = serializers.CharField(max_length=100)


#     def create(self, validated_data):
#         return Comment(**validated_data)

#     def update(self, instance, validated_data):
#         instance.email = validated_data.get('email', instance.email)
#         instance.content = validated_data.get('content', instance.content)
#         instance.created = validated_data.get('created', instance.created)
#         return instance



class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=100)
    # password = serializers.CharField(max_length=100)

    # image = serializers.ImageField(required=False)
    
    addressline1 = serializers.CharField(max_length=100,required=False)
    addressline2 = serializers.CharField(max_length=100,required=False)
    country = serializers.CharField(max_length=100,required=False)
    state = serializers.CharField(max_length=100,required=False)
    city = serializers.CharField(max_length=100,required=False)
    postalcode = serializers.CharField(max_length=100,required=False)

    dateofbirth = serializers.DateField(required=False)

    # uniquelink = serializers.CharField(max_length=100,required=False)
    # starttime = serializers.DateTimeField(required=False)
    # expiretime = serializers.DateTimeField(required=False)

    
    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance


class SupplierJobSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)
    fromcountry = serializers.CharField(max_length=100)
    fromcity = serializers.CharField(max_length=100)
    departureairport = serializers.CharField(max_length=100)
    departuredate = serializers.DateField(required=False)
    departuretime = serializers.TimeField(required=False)
    tocountry = serializers.CharField(max_length=100,required=False)
    tocity = serializers.CharField(max_length=100,required=False)
    destinationairport = serializers.CharField(max_length=100,required=False)
    arrivaldate = serializers.DateField(required=False)
    arrivaltime = serializers.TimeField(required=False)
    unusedluggage = serializers.CharField(max_length=100,required=False)
    flightno = serializers.CharField(max_length=100,required=False)
    ticketno = serializers.CharField(max_length=100,required=False)
    ticket = serializers.FileField(required=False)

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

class CustomerJobSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100,required=False)
    name = serializers.ReadOnlyField(source='user.user.name')
    phone = serializers.ReadOnlyField(source='user.user.phone')
    pickupaddress = serializers.CharField(max_length=100,required=False)
    additionaladdress = serializers.CharField(max_length=100,required=False)
    fromcountry = serializers.CharField(max_length=100,required=False)
    fromcity = serializers.CharField(max_length=100,required=False)
    frompostalcode = serializers.CharField(max_length=100,required=False)
    frompickupoption = serializers.CharField(max_length=100,required=False)
    pickupdate = serializers.DateField(required=False)
    pickuptime = serializers.TimeField(required=False)
    receivername = serializers.CharField(max_length=100,required=False)
    receiverphone = serializers.CharField(max_length=100,required=False)
    receiverdropaddress = serializers.CharField(max_length=100,required=False)
    receiveradditionaladdress = serializers.CharField(max_length=100,required=False)
    tocountry = serializers.CharField(max_length=100,required=False)
    tocity = serializers.CharField(max_length=100,required=False)
    topostalcode = serializers.CharField(max_length=100,required=False)
    topickupoption = serializers.CharField(max_length=100,required=False)
    parcellength = serializers.CharField(max_length=100,required=False)
    parcelheight = serializers.CharField(max_length=100,required=False)
    parcelwidth = serializers.CharField(max_length=100,required=False)

    parcelweight = serializers.CharField(max_length=100,required=False)
    parcelvolweight = serializers.CharField(max_length=100,required=False)
    parceltype = serializers.CharField(max_length=100,required=False)
    parcelvalue = serializers.CharField(max_length=100,required=False)
    insurance = serializers.CharField(max_length=100,required=False)
    description = serializers.CharField(max_length=500,required=False)
    parcel_id = serializers.CharField(max_length=100,required=False)
    requestSend = serializers.CharField(max_length=100,required=False)
    requestAccept = serializers.CharField(max_length=100,required=False)
    requestReject = serializers.CharField(max_length=100,required=False)
    requestPaid = serializers.CharField(max_length=100,required=False)
    # parcelstatus = serializers.StringRelatedField(many=True)
    # items = serializers.RelatedField(read_only=True,many=True)

    # class Meta:
    #     model = CustomerJob
    #     fields = ( 'items')

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

class ParcelTypeSeralizer(serializers.Serializer):
    type = serializers.CharField(max_length=100,required=False)

     
    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

class TravelByListSeralizer(serializers.Serializer):
    vehical = serializers.CharField(max_length=100,required=False)
    id = serializers.CharField(max_length=100,required=False)
     
    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

class CountrySeralizer(serializers.Serializer):
    name = serializers.CharField(max_length=100,required=False)
    id = serializers.CharField(max_length=100,required=False)
     
    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

class CitySeralizer(serializers.Serializer):
    name = serializers.CharField(max_length=100,required=False)
    id = serializers.CharField(max_length=100,required=False)
     
    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance



class AirdelyFacilitySeralizer(serializers.Serializer):
    collectioncentrename = serializers.CharField(max_length=100,required=False)
    id = serializers.CharField(max_length=100,required=False)

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance



class AirportSeralizer(serializers.Serializer):
    name = serializers.CharField(max_length=100,required=False)
     
    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance


class DocumentSerializer(serializers.Serializer):
    idproof = serializers.FileField(required=False)
    passport = serializers.FileField(required=False)

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

class BankDetailsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,required=False)
    bankname = serializers.CharField(max_length=100,required=False)
    bankbranch = serializers.CharField(max_length=100,required=False)
    accountnumber = serializers.CharField(max_length=100,required=False)
    
    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance


class NotificationSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100,required=False)
    
    forcustomer = serializers.BooleanField(required=False)
    forsupplier = serializers.BooleanField(required=False)
    related_job_id = serializers.CharField(max_length=100,required=False)
    notificationtype = serializers.CharField(max_length=100,required=False)
    text = serializers.CharField(max_length=100,required=False)
    status = serializers.CharField(max_length=100,required=False)
    

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

class CustomerJobStatusSerializer(serializers.Serializer):
    job = serializers.CharField(max_length=100,required=False)
    name = serializers.ReadOnlyField(source='job.user.user.name')
    phone = serializers.ReadOnlyField(source='job.user.user.phone')
    pickupaddress = serializers.ReadOnlyField(source='job.pickupaddress')
    additionaladdress = serializers.ReadOnlyField(source='job.additionaladdress')
    fromcountry = serializers.ReadOnlyField(source='job.fromcountry')
    fromcity = serializers.ReadOnlyField(source='job.fromcity')
    frompostalcode = serializers.ReadOnlyField(source='job.frompostalcode')
    frompickupoption = serializers.ReadOnlyField(source='job.frompickupoption')
    pickupdate = serializers.ReadOnlyField(source='job.pickupdate')

    pickuptime = serializers.ReadOnlyField(source='job.pickuptime')
    receivername = serializers.ReadOnlyField(source='job.receivername')
    receiverphone = serializers.ReadOnlyField(source='job.receiverphone')
    receiverdropaddress = serializers.ReadOnlyField(source='job.receiverdropaddress')
    receiveradditionaladdress = serializers.ReadOnlyField(source='job.receiveradditionaladdress')
    tocountry = serializers.ReadOnlyField(source='job.tocountry')
    tocity = serializers.ReadOnlyField(source='job.tocity')
    topostalcode = serializers.ReadOnlyField(source='job.topostalcode')

    topickupoption = serializers.ReadOnlyField(source='job.topickupoption')
    parcellength = serializers.ReadOnlyField(source='job.parcellength')
    parcelheight = serializers.ReadOnlyField(source='job.parcelheight')
    parcelwidth = serializers.ReadOnlyField(source='job.parcelwidth')
    parcelweight = serializers.ReadOnlyField(source='job.parcelweight')
    parcelvolweight = serializers.ReadOnlyField(source='job.parcelvolweight')
    parceltype = serializers.ReadOnlyField(source='job.parceltype')
    parcelvalue = serializers.ReadOnlyField(source='job.parcelvalue')
    insurance = serializers.ReadOnlyField(source='job.insurance')
    description = serializers.ReadOnlyField(source='job.description')

    bookingreceived = serializers.BooleanField(required=False)
    bookingconfirmed = serializers.BooleanField(required=False)
    pickupassigned = serializers.BooleanField(required=False)
    itemspicked = serializers.BooleanField(required=False)
    itemsreceived = serializers.BooleanField(required=False)
    assignedtoairtraveller = serializers.BooleanField(required=False)
    intransit = serializers.BooleanField(required=False)
    atdestinationhub = serializers.BooleanField(required=False)
    outfordelivery = serializers.BooleanField(required=False)
    itemsdelivered = serializers.BooleanField(required=False)

# class SupplierJobSerializer(serializers.Serializer):
#     job = serializers.CharField(max_length=100,required=False)
#     name = serializers.ReadOnlyField(source='job.user.user.name')
#     phone = serializers.ReadOnlyField(source='job.user.user.phone')
#     traveller_id = serializers.CharField(max_length=100,required=False)
#     status = serializers.CharField(max_length=100,required=False)
#     fromcountry = serializers.CharField(max_length=100,required=False)
#     fromcity = serializers.CharField(max_length=100,required=False)
    
#     tocountry = serializers.CharField(max_length=100,required=False)
#     tocity = serializers.CharField(max_length=100,required=False)
#     departuredate = serializers.DateField(max_length=100,required=False)

#     departuretime = serializers.TimeField(max_length=100,required=False)
#     arrivaldate = serializers.DateField(max_length=100,required=False)
#     arrivaltime = serializers.TimeField(max_length=100,required=False)
#     unusedluggage = serializers.CharField(max_length=100,required=False)
#     flightno = serializers.CharField(max_length=100,required=False)
#     ticketno = serializers.CharField(max_length=100,required=False)
#     ticket = serializers.FileField(max_length=100,required=False)
    


