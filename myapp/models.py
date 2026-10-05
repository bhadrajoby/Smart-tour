from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class agency_table(models.Model):
    login=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    logo=models.FileField()
    status=models.CharField(max_length=100)
    licence=models.FileField()

class guide_table(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.BigIntegerField()
    email = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    status = models.CharField(max_length=100)
    photo=models.FileField()

class place_table(models.Model):
    name=models.CharField(max_length=100)
    lattitude=models.FloatField()
    longitude=models.FloatField()
    type=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    photo=models.FileField()
    photo1=models.FileField()
    photo2=models.FileField()
    status=models.CharField(max_length=100)
    description=models.TextField()
    AGENCY=models.ForeignKey(agency_table,on_delete=models.CASCADE,null=True,blank=True)



class Pakages_table(models.Model):
    name=models.CharField(max_length=100)
    PLACE=models.ForeignKey(place_table,on_delete=models.CASCADE,null=True,blank=True)
    noofdays=models.CharField(max_length=100)
    photo=models.FileField()
    amount=models.CharField(max_length=100)
    description=models.TextField()



class Pakage_details_table(models.Model):
    PAKAGE=models.ForeignKey(Pakages_table,on_delete=models.CASCADE,null=True,blank=True)
    day=models.CharField(max_length=100)
    photo=models.FileField()
    place=models.CharField(max_length=100)
    details=models.CharField(max_length=1000)


class google_details(models.Model):
    PLACE = models.ForeignKey(place_table, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField()


class user_table(models.Model):
    login=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    photo = models.FileField()

class complaint_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    compliant=models.CharField(max_length=100)
    date=models.DateField()
    reply=models.CharField(max_length=100)

class notification_table(models.Model):
    date=models.DateField()
    notification=models.CharField(max_length=100)

class feedback_table(models.Model):
    user=models.ForeignKey(user_table,on_delete=models.CASCADE)
    date = models.DateField()
    feedback=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)

class moments_table(models.Model):
    user=models.ForeignKey(user_table,on_delete=models.CASCADE)
    date = models.DateField()
    description=models.CharField(max_length=100)
    image=models.FileField()
    type=models.CharField(max_length=15)

class request_table(models.Model):
    agency=models.ForeignKey(agency_table,on_delete=models.CASCADE)
    user=models.ForeignKey(user_table,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=100)

class chat_table(models.Model):
    FROMID= models.ForeignKey(User,on_delete=models.CASCADE,related_name="Fromid")
    TOID= models.ForeignKey(User,on_delete=models.CASCADE,related_name="Toid")
    message=models.CharField(max_length=100)
    date=models.DateField()


class booking_table(models.Model):
    PAKAGE=models.ForeignKey(Pakages_table,on_delete=models.CASCADE)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=100)

# class placefeedback_table(models.Model):
#     USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
#     PLACE=models.ForeignKey(place_table,on_delete=models.CASCADE)
#     date = models.DateField()
#     feedback=models.CharField(max_length=100)
#     rating=models.CharField(max_length=100)
#     photo=models.FileField()
#     emotion=models.CharField(max_length=15)



class placefeedback_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    PLACE=models.ForeignKey(place_table,on_delete=models.CASCADE)
    date = models.DateField()
    feedback=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)
    # photo=models.FileField()
    # emotion=models.CharField(max_length=15)

class agencyfeedback_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    AGENCY=models.ForeignKey(agency_table,on_delete=models.CASCADE)
    date = models.DateField()
    rating=models.CharField(max_length=100)


class emergency_alert_table(models.Model):
    user=models.ForeignKey(user_table,on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()
    date = models.DateField()
    alert=models.CharField(max_length=100)

class instruction_table(models.Model):
    GUIDE=models.ForeignKey(guide_table,on_delete=models.CASCADE)
    instruction = models.CharField(max_length=100)
    date=models.DateField()

class assign_table(models.Model):
    GUIDE=models.ForeignKey(guide_table,on_delete=models.CASCADE)
    BOOKING=models.ForeignKey(booking_table,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=100, default='assigned')


class guide_complaint_table(models.Model):
    GUIDE = models.ForeignKey(guide_table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    compliant = models.CharField(max_length=100)
    date = models.DateField()
    reply = models.CharField(max_length=100)

class non_popular_table(models.Model):
    name=models.CharField(max_length=100)
    lattitude = models.FloatField()
    longitude = models.FloatField()
    photo=models.FileField()
    category=models.CharField(max_length=100)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)


