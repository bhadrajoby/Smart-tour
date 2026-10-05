from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group


# Create your views here.
from myapp.models import *


def admin_index(request):
    return render(request,"admin/admin_home.html")

def login_page_get(request):
    return render(request,"index.html")

def login_post(request):
    mail=request.POST['username']
    pwd=request.POST['password']

    user=authenticate(request,username=mail,password=pwd)
    if user is not None:
        login(request,user)
        if user.groups.filter(name="Admin").exists():
            # messages.success(request,'Welcome Admin....!!!')
            return redirect('/myapp/admin_index/')
        elif user.groups.filter(name="Agency").exists():
            if agency_table.objects.get(login=user).status == "Accepted":
                return HttpResponse("<script>alert('Welcome Agency....!!!');window.location='/myapp/agency_home/'</script>")
            else:
                messages.error(request, 'your agency is not Authorised....!!!')
                return HttpResponse("<script>alert('your agency is not Authorised....!!!');window.location='/myapp/login_page/'</script>")

        else:
            messages.error(request,'Wrong username and password....!!!')
            return HttpResponse("<script>alert('Wrong username and password....!!!');window.location='/myapp/login_page/'</script>")

    else:
        messages.error(request, 'User not found....!!!')
        return HttpResponse("<script>alert('User not found....!!!');window.location='/myapp/login_page/' </script>")


def logout_get(request):
    logout(request)
    return redirect('/myapp/login_page/')
def admin_delete_notification(request,id):
    a=notification_table.objects.get(id=id)
    a.delete()
    return redirect('/myapp/view_notification_get/')


def change_password_get(request):
    return render(request,"admin/change_password.html")

def admin_changepassword_post(request):
    currentpassword=request.POST['old']
    newpassword=request.POST['new']
    confirmpassword=request.POST['new1']
    user=request.user
    if not check_password(currentpassword,user.password):
        messages.error(request,'current password is not correct....!')
        return redirect('/myapp/admin_change_password/')
    if newpassword==confirmpassword:
        user.set_password(newpassword)
        user.save()
        messages.error(request,'Password changed successfully')
        return redirect('/myapp/login_get')
    else:
        messages.error(request,'Password does not match....!')
        return redirect('/myapp/admin_change_password/')

def send_notification_get(request):
    return render(request,"admin/send_notification.html")

def send_notification_post(request):
    notification=request.POST['notification']

    a=notification_table()
    a.notification=notification
    a.date=datetime.now()
    a.save()
    return redirect('/myapp/send_notification_get')

def verify_agency_get(request):
    data= agency_table.objects.all()
    return render(request,"admin/verify_agency.html",{'data':data})


def accept_agency(request,id):
    d=agency_table.objects.get(id=id)
    d.status="Accepted"
    d.save()
    return redirect('/myapp/verify_agency_get/')

def reject_agency(request,id):
    d=agency_table.objects.get(id=id)
    d.status="Rejected"
    d.save()
    return redirect('/myapp/verify_agency_get/')

def view_complaint_get(request):
    data=complaint_table.objects.all()
    return render(request,"admin/view_complaint.html",{'data':data})

def admin_reply(request,id):
    a=complaint_table.objects.get(id=id)
    return render(request,'admin/send_reply_for_complaint.html',{'data':a})

def admin_reply_post(request,id):
    a=complaint_table.objects.get(id=id)
    a.reply=request.POST['reply']
    a.save()
    return redirect('/myapp/view_complaint_get/')

def view_emergency_alert_get(request):
    data=emergency_alert_table.objects.all()
    return render(request,"admin/view_emergency_alert.html",{'data':data})

def view_feedback_get(request):
    data=placefeedback_table.objects.all()
    return render(request,"admin/view_feedback.html",{'data':data})

def admin_view_feed(request):
    a=agencyfeedback_table.objects.all()
    return render(request,'admin/agency_fee.html',{'data':a})

def view_places_get(request):
    data=place_table.objects.all()
    return render(request,"admin/view_places.html",{'data':data})

def view_non_popular(request):
    data=non_popular_table.objects.all()
    return render(request,'admin/view_nonpopular_places.html',{'data':data})

def view_notification_get(request):
    data=notification_table.objects.all()
    return render(request,"admin/view_notification.html",{'data':data})

def verified_agency(request):
    data=agency_table.objects.filter(status="Accepted")
    return render(request,"admin/verified_agency.html",{'data':data})


# -------------agency----------
def register(request):
    return render(request,"agency/register.html")

def register_post(request):
    name=request.POST["name"]
    place=request.POST["place"]
    post=request.POST["post"]
    pin=request.POST["pin"]
    email=request.POST["email"]
    phone=request.POST["phone"]
    logo=request.FILES["logo"]
    licence=request.FILES["licence"]
    username=request.POST["username"]
    password=request.POST["password"]


    fs = FileSystemStorage()
    path1 = fs.save(logo.name, logo)
    path2 = fs.save(licence.name, licence)

    if User.objects.filter(username=username).exists():
        messages.warning(request, "Username Already Exists Please Choose Another One")
        return redirect('/myapp/register/')


    if User.objects.filter(email=email).exists():
        messages.warning(request, "Email Already Exists Please Use Another One")
        return redirect('/myapp/register/')

    user = User.objects.create(username=username, email=email, password = make_password(str(password)))
    user.groups.add(Group.objects.get(name='Agency'))

    k = agency_table()
    k.name = name
    k.place = place
    k.post = post
    k.pin = pin
    k.email = email
    k.phone = phone
    k.logo = path1
    k.status='Pending'
    k.licence = path2
    k.login = user
    k.save()

    messages.success(request,"Registered Successfully")
    return redirect('/myapp/register/')


def agency_view_places(request):

    places = place_table.objects.filter(AGENCY__login_id=request.user.id)
    # print(places,'places================')
    # print(places,'places================')
    # print(places,'places================')
    # print(places,'places================')

    return render(request, "agency/view_places.html", {'data': places})
def delete_place(request,id):
    a=place_table.objects.filter(id=id).delete()
    return redirect('/myapp/agency_view_places')

def edit_place(request, id):
    a = place_table.objects.get(id=id)
    return render(request, 'agency/edit_place.html', {'data': a})

def edit_places_post(request):
    name=request.POST['names']
    lattitude=request.POST['lattitude']
    longitude=request.POST['longitude']
    type=request.POST['type']
    category=request.POST['category']
    description=request.POST['description']
    status=request.POST['status']
    id=request.POST['id']
    a = place_table.objects.get(id=id)
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        f=FileSystemStorage()
        path=f.save(photo.name,photo)
        a.photo = path
        a.save()
    if 'photo1' in request.FILES:
        photo1 = request.FILES['photo1']
        f=FileSystemStorage()
        path=f.save(photo1.name,photo1)
        a.photo1 = path
        a.save()
    if 'photo2' in request.FILES:
        photo2 = request.FILES['photo2']
        f=FileSystemStorage()
        path=f.save(photo2.name,photo2)
        a.photo2 = path
        a.save()

    a.name=name
    a.lattitude=lattitude
    a.longitude=longitude
    a.type=type
    a.category=category
    a.description=description

    a.status=status
    # a.AGENCY=agency_table.objects.get(login=request.user)
    a.save()
    return redirect('/myapp/agency_view_places/')





def add_places(request):
    return render(request,"agency/add_places.html")


from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect

def add_places_post(request):
    if request.method == "POST":

        name = request.POST.get('names')
        lat = request.POST.get('lattitude')
        lon = request.POST.get('longitude')
        p_type = request.POST.get('type')
        cat = request.POST.get('category')
        stat = request.POST.get('status')
        description = request.POST.get('description')

        image1 = request.FILES.get('photo')
        image2 = request.FILES.get('photo2')
        image3 = request.FILES.get('photo3')

        fs = FileSystemStorage()

        path1 = fs.save(image1.name, image1) if image1 else None
        path2 = fs.save(image2.name, image2) if image2 else None
        path3 = fs.save(image3.name, image3) if image3 else None

        place_table.objects.create(
            name=name,
            lattitude=lat,
            longitude=lon,
            type=p_type,
            category=cat,
            photo=path1,
            photo1=path2,
            photo2=path3,
            status=stat,
            description=description,
            AGENCY=agency_table.objects.get(login_id=request.user.id)
        )

        return redirect('/myapp/agency_view_places/')

def assign_guide(request,id):
    a=booking_table.objects.get(id=id)
    b=guide_table.objects.filter(status='Active')
    return render(request,"agency/assign_guide.html",{'data':a,'data1':b})



def view_assign_guide(request):
    a=assign_table.objects.filter(BOOKING__PAKAGE__PLACE__AGENCY__login=request.user.id)
    return render(request,"agency/view assigned guide.html",{'data':a})



# def assign_guide_post(request,id):
#     guide_id=request.POST['guide']
#     a=booking_table.objects.get(id=id)
#     b=assign_table()
#     b.GUIDE=guide_table.objects.get(id=guide_id)
#     b.BOOKING=a
#     b.date=date.today()
#     b.save()
#     return redirect('/myapp/agency_view_booking')






from datetime import date
from django.http import HttpResponse
from django.shortcuts import redirect

def assign_guide_post(request, id):

    guide_id = request.POST['guide']
    booking = booking_table.objects.get(id=id)

    if assign_table.objects.filter(BOOKING=booking).exists():
        return HttpResponse(
            "<script>alert('Guide already assigned for this booking');"
            "window.location='/myapp/agency_view_booking/#a';</script>"
        )

    # Assign guide
    assign = assign_table()
    assign.GUIDE = guide_table.objects.get(id=guide_id)
    assign.BOOKING = booking
    assign.date = date.today()
    assign.save()

    return redirect('/myapp/agency_view_booking')



def AGENCY_change_password(request):
    return render(request,"agency/change_password.html")

def agency_changepassword_post(request):
    currentpassword=request.POST['old']
    newpassword=request.POST['new']
    confirmpassword=request.POST['new1']
    user=request.user
    if not check_password(currentpassword,user.password):
        messages.error(request,'current password is not correct....!')
        return redirect('/myapp/agency_home/#a')
    if newpassword==confirmpassword:
        user.set_password(newpassword)
        user.save()
        messages.error(request,'Password changed successfully')
        return redirect('/myapp/login_page')
    else:
        messages.error(request,'Password does not match....!')
        return redirect('/myapp/agency_home/')


def agency_edit_profile(request):

    a = agency_table.objects.get(login_id=request.user.id)

    return render(request,'agency/edit_profile.html',{'data':a})


def agency_edit_profile_post(request):
    name = request.POST["name"]
    place = request.POST["place"]
    post = request.POST["post"]
    pin = request.POST["pin"]
    email = request.POST["email"]
    phone = request.POST["phone"]

    k = agency_table.objects.get(login_id=request.user.id)
    fs = FileSystemStorage()

    if 'licence' in request.FILES:
        licence = request.FILES["licence"]
        path2 = fs.save(licence.name, licence)
        k.licence = path2

    if 'logo' in request.FILES:
        logo = request.FILES["logo"]
        path1 = fs.save(logo.name, logo)
        k.logo = path1

    k.name = name
    k.place = place
    k.post = post
    k.pin = pin
    k.email = email
    k.phone = phone
    k.save()

    messages.success(request, "Edited Successfully")
    return redirect('/myapp/view_profile/')

def edit_places(request):
    return render(request,"agency/edit_place.html")

def send_reply(request,id):
    var=complaint_table.objects.get(id=id)
    request.session['id']=id
    return render(request,"agency/send_reply.html")

def send_reply_post(request):
    reply=request.POST['reply']
    var=complaint_table.objects.get(id=request.session['id'])
    var.reply=reply
    var.save()

    return redirect('/myapp/view_complaint/#a')

def verify_guide(request):
    a = guide_table.objects.all()
    return render(request,"agency/verify_guide.html",{'data':a})

def agency_accept_guide(request,id):
    a=guide_table.objects.get(id=id)
    a.status='Active'
    a.save()
    return redirect('/myapp/verify_guide/')

def agency_reject_guide(request,id):
    l=guide_table.objects.get(id=id)
    l.status='Blocked'
    l.save()
    return redirect('/myapp/verify_guide')

def verified_guide(request):
    a=guide_table.objects.filter(status='Active')
    return render(request,"agency/verified_guide.html",{'data':a})

def view_complaint(request):
    a=agency_table.objects.get(login=request.user)
    b=complaint_table.objects.filter(agency=a)
    return render(request,"agency/view_complaint.html",{'data':b})

def view_emergency_alert(request):
    a=emergency_alert_table.objects.all()
    return render(request,"agency/view_emergency_alert.html",{'data':a})

def agency_view_instruction(request):
    return render(request,"agency/view_instruction.html")


def view_request_and_verify(request):
    return render(request,"agency/view_request_and_verify.html")

def agency_home(request):
    return render(request,"agency/agency_home.html")

def view_profile(request):
    a=agency_table.objects.get(login=request.user)
    return render(request,"agency/view_profile.html",{'data':a})

def agency_view_booking(request):
    a=booking_table.objects.filter(PAKAGE__PLACE__AGENCY__login_id=request.user.id)

    return render(request,'agency/view_user_booking.html',{'data':a})

# --------------------guide-----------



def android_login(request):
    username=request.POST['Username']
    password=request.POST['Password']
    user=authenticate(request,username=username,password=password)
    if user is not None:
        if user.groups.filter(name='Guide').exists():
            if guide_table.objects.get(login=user).status =="Active":
                return JsonResponse({'status': 'ok', 'lid': str(user.id), 'type': 'Guide'})
            else:
                return JsonResponse({'status': 'pending', 'lid': str(user.id), 'type': 'Guide'})


        elif user.groups.filter(name='U_ser').exists():
            login(request,user)
            return JsonResponse({'status':'ok','lid':str(user.id),'type':'U_ser'})

        else:
            return JsonResponse({'status':'not ok'})
    else:
        return JsonResponse({'status':'not ok'})


def guide_register_post(request):
    name=request.POST["name"]
    place=request.POST["place"]
    post=request.POST["post"]
    pin=request.POST["pin"]
    email=request.POST["email"]
    phone=request.POST["phone"]
    photo=request.FILES["photo"]
    longitude=request.POST["longitude"]
    latitude=request.POST["latitude"]
    password=request.POST["password"]
    cpassword=request.POST["cpassword"]

    fs=FileSystemStorage()
    path=fs.save(photo.name,photo)

    if password != cpassword:
        return JsonResponse({'status': 'failed', 'message': 'password does not match'})

    if User.objects.filter(username=email).exists():
        return JsonResponse({'status': 'failed','message':'username already exists'})




    user = User.objects.create(username=email, email=email, password = make_password(str(password)))
    user.groups.add(Group.objects.get(name='Guide'))

    k = guide_table()
    k.name = name
    k.place = place
    k.post = post
    k.pin = pin
    k.email = email
    k.phone = phone
    k.photo=path
    k.longitude = longitude
    k.latitude=latitude
    k.status = 'Pending'
    k.login = user
    k.save()


    return JsonResponse({'status': 'ok', 'message': 'successfully registered'})


def guide_change(request):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    lid = request.POST['lid']
    a= User.objects.get(id=lid)
    if new_password == confirm_password:
        pas = check_password(current_password,a.password)
        if pas:
            a.set_password(new_password)
            a.save()

            return JsonResponse ({'key':'Password Changed'})
        else:


            return JsonResponse({'key':'Incorrect Password'})
    else:


        return JsonResponse({'key':'Dismatch password'})


from django.http import JsonResponse
from .models import place_table, agency_table

def view_guide_places(request):
    if request.method == "POST":
        places = place_table.objects.all()

        data = []

        for place in places:
            data.append({
                "id": place.id,
                "name": place.name,
                "lattitude": place.lattitude,
                "longitude": place.longitude,
                "type": place.type,
                "category": place.category,
                "photo": place.photo.url if place.photo else "",
                "status": place.status,
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })

def guide_view_profile(request):
    lid=request.POST['lid']
    a=guide_table.objects.get(login_id=lid)
    data=[]
    data.append({
        'id':a.id,
        'name':a.name,
                 'place':str(a.place),
                 'post':str(a.post),
                 'pin':str(a.pin),
                 'email':str(a.email),
                 'phone':str(a.phone),
                 'longitude':str(a.longitude),
                 'latitude':str(a.latitude),
                'photo':str(a.photo.url),
                 'status':str(a.status),

                 })

    return JsonResponse({'status':'Success','data':data})






def view_assign(request):
    lid = request.POST['lid']
    a = assign_table.objects.filter(GUIDE__login_id=lid)
    data = []
    for i in a:
        data.append({
                      'id':str(i.id),
                     'PACKAGE': str(i.BOOKING.PAKAGE.name),
                     'USER':str(i.BOOKING.USER.name),
                     'email':str(i.BOOKING.USER.email),
                     'phone':str(i.BOOKING.USER.phone),
                     'date': str(i.date),
                     'status': str(i.status),
                     })
    print(data,'=======================')
    return JsonResponse({'status':'Success','data':data})

def add_instruction(request):
    instruction = request.POST['instruction']
    lid=request.POST['lid']
    a=guide_table.objects.get(login_id=lid)
    l=instruction_table()
    l.instruction = instruction
    l.date = date.today()
    l.GUIDE_id=a.id
    l.save()
    return JsonResponse({'status': 'ok', 'message': 'successfully added'})


def guide_view_instruction(request):
    lid = request.POST['lid']
    print(lid,'lid')
    a = guide_table.objects.get(login_id=lid)
    l = instruction_table.objects.filter(GUIDE=a)
    data = []
    for i in l:
        data.append({'id':i.id,'instruction': str(i.instruction),
                 'date': str(i.date),
                 })
    return JsonResponse({'status':'ok','data':data})


def guide_instructionviewforedit(request):
    inst_id=request.POST['inst_id']
    print('liddddddddddd',inst_id)
    i=instruction_table.objects.get(id=inst_id)
    return JsonResponse ({'status':'ok',"name":str(i.instruction),})


def edit_instruction(request):
    inst_id=request.POST['inst_id']

    name=request.POST['name']

    i= instruction_table.objects.get(id=inst_id)
    i.instruction=name
    i.save()
    return JsonResponse({'status':'ok','message':'Edited Successfully'})


def guide_profileviewforedit(request):
    lid=request.POST['lid']
    print('liddddddddddd',lid)
    a=guide_table.objects.get(login_id=lid)
    return JsonResponse ({'status':'ok','name':str(a.name),
                 'place':str(a.place),
                 'post':str(a.post),
                 'pin':str(a.pin),
                 'email':str(a.email),
                 'phone':str(a.phone),
                 'longitude':str(a.longitude),
                 'latitude':str(a.latitude),
                          'photo': a.photo.url if a.photo else ''

                          })


def guide_edit_profile(request):
    lid=request.POST['lid']

    name=request.POST['name']
    place=request.POST['place']
    post=request.POST['post']
    pin=request.POST['pin']
    email=request.POST['email']
    phone=request.POST['phone']
    longitude=request.POST['longitude']
    latitude=request.POST['latitude']

    i= guide_table.objects.get(login_id=lid)

    i.name=name
    i.place=place
    i.post=post
    i.pin=pin
    i.email=email
    i.phone=phone
    i.longitude=longitude
    i.latitude=latitude

    if 'photo' in request.FILES:
        photo = request.FILES['photo']

        if i.photo:
            if default_storage.exists(i.photo.name):
                default_storage.delete(i.photo.name)
        i.photo.save(photo.name, photo)

    i.save()
    return JsonResponse({'status':'ok','message':'Edited Successfully'})


def guide_delete_instruction(request):
    inst_id = request.POST['inst_id']
    v = instruction_table.objects.get(id=inst_id)
    v.delete()
    return JsonResponse({'status':'ok','message':'Deleted Successfully'})






# -----------user----------



def user_register_post(request):
    name=request.POST["name"]
    email=request.POST["email"]
    phone=request.POST["phone"]
    place=request.POST["place"]
    post=request.POST["post"]
    photo=request.FILES["photo"]
    password=request.POST["password"]
    cpassword=request.POST["cpassword"]
    fs=FileSystemStorage()
    path=fs.save(photo.name,photo)
    if password != cpassword:
        return JsonResponse({'status': 'failed', 'message': 'password does not match'})

    if User.objects.filter(username=email).exists():
        return JsonResponse({'status': 'failed','message':'username already exists'})




    user = User.objects.create(username=email, email=email, password = make_password(str(password)))
    user.groups.add(Group.objects.get(name='U_ser'))

    k = user_table()
    k.name = name
    k.email = email
    k.phone = phone
    k.place = place
    k.post = post
    k.photo = path
    k.latitude = 11.56789
    k.longitude = 73.56789

    k.status = 'Pending'
    k.login = user
    k.save()


    return JsonResponse({'status': 'ok', 'message': 'successfully registered'})

def user_search_places(request):
        places = place_table.objects.all()
        # print(places.photo.url)

        data = []

        for place in places:
            data.append({
                "id": place.id,
                "name": place.name,
                "lattitude": place.lattitude,
                "longitude": place.longitude,
                "type": place.type,
                "category": place.category,
                "photo": place.photo.url,
                "status": place.status,
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })

def user_search_agency(request):
    agencies = agency_table.objects.all()
    data = []
    for agency in agencies:
        data.append({
            "id": agency.id,
            "name": agency.name,
            "place": agency.place,
            "post": agency.post,
            "pin": agency.pin,
            "email": agency.email,
            "phone": agency.phone,
            "logo": agency.logo.url,
            "status": agency.status,
        })

    return JsonResponse({
        "status": "success",
        "data": data
    })

from datetime import datetime
def send_complaint(request):
    com = request.POST['compliant']

    s = complaint_table()

    s.compliant = com
    s.date = datetime.now().today()
    s.reply = 'pending'
    s.user_id = request.POST['lid']
    s.save()
    return JsonResponse({'status':'ok'})

def user_view_complaint(request):
    lid = request.POST['lid']
    a = complaint_table.objects.filter(user_id=lid)
    data=[]
    for i in a:
        data.append({
            'id':str(i.id),
            'compliants':str(i.compliant),
            'reply':str(i.reply),
            'date':str(i.date),
        })
    print(data)
    return JsonResponse({'status':'ok','data':data})

def view_user_places(request):
    if request.method == "POST":
        places = place_table.objects.all()

        data = []

        for place in places:
            data.append({
                "id": place.id,
                "name": place.name,
                "lattitude": place.lattitude,
                "longitude": place.longitude,
                "type": place.type,
                "category": place.category,
                "photo": place.photo.url,
                "photo1": place.photo1.url,
                "photo2": place.photo2.url,
                "status": place.status,
                "description": place.description,
                "AGENCY": str(place.AGENCY.name),
                "phone": str(place.AGENCY.phone),
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })







def view_user_beach_places(request):
    if request.method == "POST":
        places = place_table.objects.filter(category='Beach')

        data = []

        for place in places:
            data.append({
                "id": place.id,
                "name": place.name,
                "lattitude": str(place.lattitude),
                "longitude": str(place.longitude),
                "type": place.type,
                "category": place.category,
                "photo": place.photo.url,
                "photo1": place.photo1.url,
                "photo2": place.photo2.url,
                "status": place.status,
                "description": place.description,
                "AGENCY": str(place.AGENCY.name),
                "phone": str(place.AGENCY.phone),
            })
        print(data)
        return JsonResponse({
            "status": "success",
            "data": data
        })




def view_user_city_places(request):
    if request.method == "POST":
        places = place_table.objects.filter(category='City')

        data = []

        for place in places:
            data.append({
                "id": place.id,
                "name": place.name,
                "lattitude": str(place.lattitude),
                "longitude": str(place.longitude),
                "type": place.type,
                "category": place.category,
                "photo": place.photo.url,
                "photo1": place.photo1.url,
                "photo2": place.photo2.url,
                "status": place.status,
                "description": place.description,
                "AGENCY": str(place.AGENCY.name),
                "phone": str(place.AGENCY.phone),
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })

def view_user_desert_places(request):
    if request.method == "POST":
        places = place_table.objects.filter(category='Desert')

        data = []

        for place in places:
            data.append({
                "id": place.id,
                "name": place.name,
                "lattitude": str(place.lattitude),
                "longitude": str(place.longitude),
                "type": place.type,
                "category": place.category,
                "photo": place.photo.url,
                "photo1": place.photo1.url,
                "photo2": place.photo2.url,
                "status": place.status,
                "description": place.description,
                "AGENCY": str(place.AGENCY.name),
                "phone": str(place.AGENCY.phone),
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })
def view_user_hills_places(request):
    if request.method == "POST":
        places = place_table.objects.filter(category='Hills')

        data = []

        for place in places:
            data.append({
                "id": place.id,
                "name": place.name,
                "lattitude": str(place.lattitude),
                "longitude": str(place.longitude),
                "type": place.type,
                "category": place.category,
                "photo": place.photo.url,
                "photo1": place.photo1.url,
                "photo2": place.photo2.url,
                "status": place.status,
                "description": place.description,
                "AGENCY": str(place.AGENCY.name),
                "phone": str(place.AGENCY.phone),
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })


from datetime import datetime
def send_feedback_user(request):
    pid=request.POST['pid']
    lid=request.POST['lid']
    rating=request.POST['rating']
    photo=request.POST['photo']
    a=user_table.objects.get(login=lid)
    b=place_table.objects.get(id=pid)

    feedback = request.POST['feedback']

    s = placefeedback_table()

    s.USER = a
    s.PLACE = b
    s.date = datetime.now().today()
    s.feedback = feedback
    s.rating = rating
    s.photo = photo
    s.save()
    return JsonResponse({'status':'ok'})





def add_moments(request):
    if request.method == "POST":

        lid = request.POST.get('lid')
        description = request.POST.get('description')
        type = request.POST.get('type')

        user = user_table.objects.get(login_id=lid)

        fs = FileSystemStorage()
        path = None

        # If Image
        if type == "image" and 'image' in request.FILES:
            image = request.FILES['image']
            path = fs.save(image.name, image)

        # If Video
        elif type == "video" and 'file' in request.FILES:
            video = request.FILES['file']
            path = fs.save(video.name, video)

        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid file'})

        moment = moments_table()
        moment.user = user
        moment.date = datetime.now().date()
        moment.description = description
        moment.type = type
        moment.image = path   # You can rename this field to media if needed
        moment.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'})


def view_memories_user(request):
    if request.method == "POST":
        lid=request.POST['lid']
        a=user_table.objects.get(login=lid)
        moment = moments_table.objects.filter(user=a)

        data = []

        for m in moment:
            data.append({
                "id": m.id,
                "date": str(m.date),
                "description": str(m.description),
                "file":str(m.image.url),
                "type": str(m.type)

            })

        return JsonResponse({
            "status": "success",
            "data": data
        })





def user_view_agency(request):
    agencies = agency_table.objects.all()
    data = []
    for agency in agencies:
        data.append({
            "id": agency.id,
            "name": agency.name,
            "place": agency.place,
            "post": agency.post,
            "pin": agency.pin,
            "email": agency.email,
            "phone": agency.phone,
            "logo": agency.logo.url,
            "status": agency.status,
            "agencylid": agency.login_id,
        })

    return JsonResponse({
        "status": "success",
        "data": data
    })


def send_agencyfeedback_user(request):
    aid=request.POST['aid']
    lid=request.POST['lid']
    rating=request.POST['rating']

    a=user_table.objects.get(login=lid)
    b=agency_table.objects.get(id=aid)



    s = agencyfeedback_table()

    s.USER = a
    s.AGENCY = b
    s.date = datetime.now().today()

    s.rating = rating

    s.save()
    return JsonResponse({'status':'ok'})




def user_to_expert_chatview(request):
    fromid = request.POST["from_id"]
    expert_id = request.POST.get("to_id")

    print(fromid)

    # # lmid = request.POST["lastmsgid"]    from django.db.models import Q
    # expert id= Expert.objects.get(id=expert_id)
    toid = expert_id
    res = chat_table.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by("id")
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})

    return JsonResponse({"status":"ok",'data':l})




def user_to_expert_sendchat(request):
    FROM_id=request.POST['from_id']
    expert_id=request.POST['to_id']
    print(expert_id,'sldkfnlkdmfdfm')
    print(FROM_id,'from_id')
    print(expert_id,'exp_to_id')
    msg=request.POST['message']

    TOID_id = expert_id
    print(TOID_id, 'TOID_id')

    from  datetime import datetime
    c=chat_table()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def user_view_profile(request):
    lid=request.POST['lid']
    # photo = request.POST['photo']
    a=user_table.objects.get(login_id=lid)

    data=[]
    data.append({
        'id':a.id,
        'name':a.name,
                 'email':a.email,
                 'phone':a.phone,
                 'place':a.place,
                 'post':a.post,
                 'photo':a.photo.url
                 })

    return JsonResponse({'status':'Success','data':data})


# views.py
from django.http import JsonResponse
from .models import user_table
from django.core.files.storage import default_storage


def user_profileviewforedit(request):
    lid = request.POST.get('lid')
    try:
        user = user_table.objects.get(login_id=lid)
        return JsonResponse({
            'status': 'ok',
            'name': user.name,
            'place': user.place,
            'email': user.email,
            'phone': user.phone,
            'post': user.post,
            'photo': user.photo.url if user.photo else ''
        })
    except user_table.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})


def user_edit_profile(request):


    lid = request.POST.get('lid')
    name = request.POST.get('name')
    place = request.POST.get('place')
    post = request.POST.get('post')
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    try:
        user = user_table.objects.get(login_id=lid)
        user.name = name
        user.place = place
        user.post = post
        user.email = email
        user.phone = phone


        if 'photo' in request.FILES:
            photo = request.FILES['photo']

            if user.photo:
                if default_storage.exists(user.photo.name):
                    default_storage.delete(user.photo.name)
            user.photo.save(photo.name, photo)

        user.save()
        return JsonResponse({'status': 'ok', 'message': 'Edited Successfully'})

    except user_table.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
def user_add_places(request):
    lid=request.POST['lid']
    name=request.POST['names']
    lattitude=request.POST['lattitude']
    longitude=request.POST['longitude']
    category=request.POST['category']
    photo=request.FILES['photo']

    fs=FileSystemStorage()
    path=fs.save(photo.name,photo)


    a=non_popular_table()
    a.name=name
    a.lattitude=lattitude
    a.longitude=longitude
    a.category=category
    a.photo=path
    a.USER=user_table.objects.get(login_id=lid)
    a.save()
    return JsonResponse({'status':'ok','message':'Added Successfully'})

def user_view_notification(request):

    var = notification_table.objects.all()
    l = []
    for i in var:
        l.append(
            {
                'id': i.id,
                'date': str(i.date),
                'notification': str(i.notification),

            }
        )

        print(l, '============')
        print(l, '============')
        print(l, '============')
    return JsonResponse({'status': 'ok', 'data': l})
def user_view_package(request):
    pid=request.POST['id']
    var=Pakages_table.objects.filter(PLACE=pid)
    l=[]
    for i in var:
        l.append(
            {
                'id':i.id,
                'name':str(i.name),
                'PLACE':str(i.PLACE.name),
                'category':str(i.PLACE.category),
                'noofdays':str(i.noofdays),
                'amount':str(i.amount),
                'description':str(i.description),
                'photo':str(i.photo.url),
            }
        )

        print(l,'============')
        print(l,'============')
        print(l,'============')
    return JsonResponse({'status':'ok','data':l})


def user_add_booking(request):
    pid=request.POST['pid']
    lid=request.POST['lid']
    var=booking_table()
    var.USER=user_table.objects.get(login_id=lid)
    var.PAKAGE=Pakages_table.objects.get(id=pid)
    var.date=datetime.now().today().date()
    var.status='Booked'
    var.save()
    return JsonResponse({'status':'ok'})







# chat==========================


from .models import Pakages_table, place_table

def add_package(request):
    places = place_table.objects.filter(AGENCY__login_id=request.user.id)

    if request.method == "POST":
        name = request.POST.get("name")
        place_id = request.POST.get("place")
        noofdays = request.POST.get("noofdays")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        photo = request.FILES.get("photo")

        Pakages_table.objects.create(
            name=name,
            PLACE_id=place_id,
            noofdays=noofdays,
            amount=amount,
            description=description,
            photo=photo
        )

    return render(request, "agency/add_package.html", {"places": places})



def view_package(request):
    packages = Pakages_table.objects.select_related("PLACE").all()
    return render(request, "agency/view_package.html", {"packages": packages})


# DELETE PACKAGE
def delete_package(request, id):
    package =Pakages_table.objects.get(id=id)
    package.delete()
    return redirect('/myapp/view_package/')

def agency_chat_to_user(request, id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = user_table.objects.get(login=cid)
    print(qry.login.id,'login----------')

    return render(request, "agency/Chat.html", { 'name': qry.name, 'toid': cid})
    # return render(request, "shop/Chat.html", {'photo': qry.image, 'name': qry.name, 'toid': cid})

def confrim_requests(request):
    id = request.POST['id']
    assign_table.objects.filter(id = id).update(status='confirm')
    return JsonResponse({'status':'ok'})

def completed_requests(request):
    id = request.POST['id']
    assign_table.objects.filter(id = id).update(status='completed')
    return JsonResponse({'status':'ok'})

# ============================================================CHAT======
# ============================================================CHAT======

def agency_chat_with_user(request, id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = user_table.objects.get(login=cid)
    # print(qry.LOGIN.id,'login----------')
    # return render(request, "agency/Chat.html", { 'name': qry.name, 'toid': cid})
    return render(request, "agency/Chat.html", {'photo': qry.photo.url, 'name': qry.name, 'toid': cid})

def chat_view(request):
    fromid = request.user.id
    toid = request.session["userid"]
    qry = user_table.objects.get(login_id=request.session["userid"])
    from django.db.models import Q

    res = chat_table.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by('id')
    l = []
    print(qry.name,'userssssssssss')

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})

    # return JsonResponse({'photo': qry.image, "data": l, 'name': qry.name, 'toid': request.session["userid"]})
    return JsonResponse({ "data": l, 'name': qry.name, 'toid': request.session["userid"]})

def chat_send(request, msg):
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = chat_table()
    chatobt.message = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})






from django.http import JsonResponse
from django.db.models import Avg, Count

def recommend_places(request):

    lid = request.POST['lid']
    user = user_table.objects.get(login=lid)

    # Find category the user rated most
    fav_category = (
        placefeedback_table.objects
        .filter(USER=user)
        .values('PLACE__category')
        .annotate(
            total_rating=Avg('rating'),
            count=Count('id')
        )
        .order_by('-total_rating')
        .first()
    )

    if fav_category is None:
        return JsonResponse({"status": "no_data"})

    category = fav_category['PLACE__category']

    # Get recommended places from same category
    places = (
        place_table.objects
        .filter(category=category)
        .annotate(avg_rating=Avg('placefeedback_table__rating'))
        .order_by('-avg_rating')
    )

    data = []

    for place in places:
        data.append({
            "id": place.id,
            "name": place.name,
            "category": place.category,
            "type": place.type,
            "lattitude": place.lattitude,
            "longitude": place.longitude,
            "photo": place.photo.url,
            "photo1": place.photo1.url,
            "photo2": place.photo2.url,
            "description": place.description,
            "rating": place.avg_rating if place.avg_rating else 0,
            "AGENCY": str(place.AGENCY.name),
            "phone": str(place.AGENCY.phone),
        })

    return JsonResponse({
        "status": "success",
        "recommended_category": category,
        "data": data
    })





from django.http import JsonResponse
from django.db.models import Count, Avg
from .models import *

def recommend_users(request):

    lid = request.POST['lid']
    user = user_table.objects.get(login=lid)

    # categories liked by current user
    my_categories = placefeedback_table.objects.filter(
        USER=user,
        rating__gte=3.5
    ).values_list('PLACE__category', flat=True)

    # find like minded users
    users = placefeedback_table.objects.filter(
        PLACE__category__in=my_categories,
        rating__gte=3.5
    ).exclude(
        USER=user
    ).values(
        'USER__id',
        'USER__name',
        'USER__email',
        'USER__phone',
        'USER__place',
        'USER__post',
        'USER__photo',
        'PLACE__category'
    ).annotate(

        avg_rating = Avg('rating'),      # ⭐ average rating
        rating_count = Count('id')       # ⭐ number of ratings

    ).order_by(

        '-avg_rating',                   # first priority
        '-rating_count'                  # second priority

    )

    data = []

    for u in users:
        data.append({
            "uid": u['USER__id'],
            "name": u['USER__name'],
            "email": u['USER__email'],
            "phone": u['USER__phone'],
            "place": u['USER__place'],
            "post": u['USER__post'],
            "photo": "/media/" + str(u['USER__photo']),
            "category": u['PLACE__category'],
            "avg_rating": round(u['avg_rating'],1),
            "rating_count": u['rating_count']
        })

    return JsonResponse({
        "status": "success",
        "data": data
    })




from django.http import JsonResponse
from .models import *

def updatelocation(request):

    latitude = request.POST['lat']
    longitude = request.POST['lon']
    lid = request.POST['lid']

    user = user_table.objects.filter(login_id=lid)

    if user.exists():

        u = user.first()
        u.latitude = latitude
        u.longitude = longitude
        u.save()

        return JsonResponse({'status': 'updated'})

    else:

        u = user_table()
        u.login_id = lid
        u.latitude = latitude
        u.longitude = longitude
        u.save()

        return JsonResponse({'status': 'added'})




def user_view_booking(request):
    l=[]


    lid=request.POST['lid']
    var=booking_table.objects.filter(USER__login_id=lid)
    for i in var:
        l.append({
            'id':i.id,
            'noofdays':str(i.PAKAGE.noofdays),
            'photo':str(i.PAKAGE.photo.url),
            'PAKAGE':str(i.PAKAGE.name),
            'amount':str(i.PAKAGE.amount),
            'description':str(i.PAKAGE.description),
            'PLACE':str(i.PAKAGE.PLACE.name),
            'lattitude':str(i.PAKAGE.PLACE.lattitude),
            'longitude':str(i.PAKAGE.PLACE.longitude),
        })
    print(l,'data======================')
    return JsonResponse({'status': 'ok','data':l})







import requests
from django.http import JsonResponse


def user_predict_weather(request):


    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    if not latitude or not longitude:
        return JsonResponse({"status": "error", "message": "Latitude or Longitude missing"})

    API_KEY = "2c74bdea7b9d1af91c749c3a91105ff5"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    url = f"{BASE_URL}?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        return JsonResponse({"status": "error", "message": "Weather API error"})

    data = response.json()

    # -------- BASIC WEATHER DATA --------
    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")

    temperature = data.get("main", {}).get("temp", 0)
    feels_like = data.get("main", {}).get("feels_like", 0)
    humidity = data.get("main", {}).get("humidity", 0)
    pressure = data.get("main", {}).get("pressure", 0)

    wind_speed = data.get("wind", {}).get("speed", 0)
    wind_gust = data.get("wind", {}).get("gust", 0)

    description = data.get("weather", [{}])[0].get("description", "Unknown")

    rainfall = data.get("rain", {}).get("1h", 0)

    # -------- WEATHER ALERT --------
    rain_alert = "No Rain"

    if rainfall > 0 or "rain" in description.lower():
        rain_alert = "Rain Expected"

    # -------- FLOOD RISK --------
    flood_risk = "Low"

    if rainfall > 20 or humidity > 85:
        flood_risk = "Moderate"

    if rainfall > 35:
        flood_risk = "High"

    # -------- LANDSLIDE RISK --------
    landslide_risk = "Low"

    if rainfall > 30 or wind_speed > 10:
        landslide_risk = "Moderate"

    if rainfall > 50:
        landslide_risk = "High"

    # -------- CYCLONE / STORM RISK --------
    storm_risk = "Low"

    if wind_speed > 15:
        storm_risk = "Moderate"

    if wind_speed > 25:
        storm_risk = "High"

    return JsonResponse({
        "status": "ok",

        "location": f"{city}, {country}",
        "temperature": temperature,
        "feels_like": feels_like,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "wind_gust": wind_gust,
        "rainfall": rainfall,
        "description": description.capitalize(),

        # Alerts
        "rain_alert": rain_alert,

        # Disaster Predictions
        "flood_risk": flood_risk,
        "landslide_risk": landslide_risk,
        "storm_risk": storm_risk
    })



from django.http import JsonResponse
from datetime import datetime
from .models import user_table, emergency_alert_table

def user_sent_emergency_sos(request):
    lid = request.POST.get('lid')  # safer than direct dict access

    if not lid:
        return JsonResponse({"status": "error", "message": "lid is required"})

    user_record = user_table.objects.get(login_id=lid)

    alert = emergency_alert_table.objects.create(
        user=user_record,               # ← fixed: use the correct field name 'user'
        latitude=user_record.latitude,
        longitude=user_record.longitude,
        date=datetime.now().date(),
        alert="Need Help!!!"
    )

    return JsonResponse({
        "status": "ok",
        "message": "SOS Alert Sent Successfully",
        "alert_id": alert.id,           # optional - useful for debugging
        "sent_lat": float(user_record.latitude),
        "sent_lng": float(user_record.longitude)
    })






def search_package_by_price(request):

    amount = request.POST['amount']

    packages = Pakages_table.objects.filter(
        amount__lte=amount
    ).values(
        'id',
        'name',
        'noofdays',
        'amount',
        'description',
        'photo',
        'PLACE__name'
    )

    data = []

    for p in packages:
        data.append({
            "id": p['id'],
            "name": p['name'],
            "days": p['noofdays'],
            "amount": p['amount'],
            "description": p['description'],
            "photo": "/media/" + str(p['photo']),
            "place": p['PLACE__name']
        })

    return JsonResponse({
        "status": "success",
        "data": data
    })


def user_view_assigned_guide(request):


    bid=request.POST['bid']
    l=[]
    var=assign_table.objects.filter(BOOKING_id=bid)
    for i in var:
        l.append({
            'id':i.id,
            'GUIDE':str(i.GUIDE.name),
            'place':str(i.GUIDE.place),
            'phone':str(i.GUIDE.phone),
            'longitude':str(i.GUIDE.longitude),
            'latitude':str(i.GUIDE.latitude),
            'photo':str(i.GUIDE.photo.url),
        })

    print(l,'data===============')
    print(l,'data===============')
    print(l,'data===============')
    return JsonResponse({'status': 'ok','data':l})





from django.http import JsonResponse
from .models import *

def guide_updatelocation(request):

    latitude = request.POST['lat']
    longitude = request.POST['lon']
    lid = request.POST['lid']

    user = guide_table.objects.filter(login_id=lid)

    if user.exists():

        u = user.first()
        u.latitude = latitude
        u.longitude = longitude
        u.save()

        return JsonResponse({'status': 'updated'})

    else:

        u = guide_table()
        u.login_id = lid
        u.latitude = latitude
        u.longitude = longitude
        u.save()

        return JsonResponse({'status': 'added'})



from django.http import JsonResponse

def view_other_memories_user(request):
    if request.method == "POST":
        lid = request.POST.get('lid')

        moment = moments_table.objects.exclude(user__login_id=lid)

        data = []

        for m in moment:
            data.append({
                "id": m.id,
                "date": str(m.date),
                "description": str(m.description),
                "file": m.image.url if m.image else "",
                "type": str(m.type)
            })

        return JsonResponse({
            "status": "success",
            "data": data
        })




def user_view_guide_guidence(request):
    l=[]
    var=instruction_table.objects.all()
    for i in var:
        l.append({
            'id':i.id,
            'instruction':i.instruction,
            'date':str(i.date),
            'GUIDE':i.GUIDE.name

        })
    print(l)
    return JsonResponse({
        "status": "success",
        "data": l
    })
