from django.shortcuts import render, redirect
from django.http import  HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from . import models
from .helpers import auth_helpers
from .helpers import machine
from .helpers import analysis
from .helpers import sentiment
from .helpers import collocations as col
from django.utils import timezone
import nltk
import math
import os
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import LogisticRegression
from bs4 import BeautifulSoup
from sklearn.externals import joblib
import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
from nltk.corpus import webtext
from nltk.corpus import PlaintextCorpusReader
import numpy as np
from nltk import FreqDist
from hospital.models import Hospital
from django.db.models import Q

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="/hospital")
def home_view(request):
    form = auth_helpers.update_profile_entity(request)
    if auth_helpers.is_hospital(request.user):
        
        hosp = models.HospitalDetails.objects.get(hospital=models.Hospital.objects.get(user=request.user))
        review = models.Reviews.objects.filter(hospital=models.Hospital.objects.get(user=request.user))
        print (review)
        #print("BEHOLD")
        hospname=str(hosp.hospital)
        #print (hospname+"hello")
        live=[]
        file = open("/home/helios/Desktop/easclepius/easclepius/"+hospname,'a')
        print (hosp.id)
        for i in review:
            live.append(i.review)
            file.write(str(i.review)+"\n")
        file.close()
        print ("klklkkllkklklkll")
        print(col.give(hospname))
        good=col.give(hospname)
        good2=[]
        for y in good:
            good2.append(" ".join(str(x) for x in y))
        print (live)
        machine.lie(live)
        sent=machine.show_review()
        sent2=analysis.live_review(live)
        if sent2[0]>0:
            p="Positive"
        else:
            p="Negative"
        sent3=int(math.floor(sent2[0]*10))
        sent5=sent2[1]*100
        sent6=sent2[2]*100
        sent7 = sent2[3] * 100
        li=[]
        li2=[]
        return render(request, "hospital_profile.html",{'form':form,'hosp':hosp,"review":review,"sent":sent3,"sent2":sent2[0],
                                                      "sent5":sent5,"sent6":sent6,"sent7":sent7,"polarity":p,"good2":good2})
    ur=models.PatientDetails.objects.get(patient=models.Patient.objects.get(user=request.user))
    return render(request, "patient_profile.html",{'form':form,"ur":ur})


def authentication_manager(request):
    if not request.user.is_anonymous:
        return redirect("/hospital/home")
    if request.method == "GET":
        return render(request, "index.html")
    if request.method == "POST":
        req =  request.POST
        username = req["uname"]
        password = req["psw"]
        if req["meta"] == "login":
            #login logic here

            if auth_helpers.login_user(username, password, request):
                return redirect("/hospital/home")
            else:
                return redirect("/hospital")
        elif req["meta"] == "signup":

            #check if similar user exists
            if auth_helpers.signup_patient(request.POST):
                if auth_helpers.login_user(username, password, request):
                    return redirect("/hospital/home")
            return redirect("/hospital")
        else:
            #standard error page
            pass
    return redirect("/hospital")




def logout_view(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect("/hospital")


def hospital_auth(request):
    if not request.user.is_anonymous:
        return redirect("/hospital/hospital")
    if request.method == "GET":
        return render(request, "hospital_index.html")
    if request.method == "POST":
        req =  request.POST
        username = req["uname"]
        password = req["psw"]
        if req["meta"] == "login":
            #login logic here

            if auth_helpers.login_user(username, password, request):
                return redirect("/hospital/home")
            else:
                return redirect("/hospital/hospital")
        elif req["meta"] == "signup":

            #check if similar user exists
            if auth_helpers.signup_hospital(request.POST):
                if auth_helpers.login_user(username, password, request):
                    return redirect("/hospital/home")
            return redirect("/hospital/hospital")
        else:
            #standard error page
            pass
    return redirect("/hospital/hospital")

def profile_view(request,username):
    user = User.objects.get(username=username)
    #history = models.Disease.objects.filter(
        #models.MedicalHistory.objects.get(patient=models.Patient.objects.get(user=user)))
    patient = models.Patient.objects.get(user=user)
    hospital = models.Hospital.objects.get(user=request.user)
    if request.method == "POST":
        diseasetype = request.POST["diseasetype"]
        comment = request.POST["comment"]
        medicaldata = request.POST["medicaldata"]
        dis=models.Disease.objects.create(diseasetype=diseasetype,)
        data = models.MedicalHistory.objects.create(patient=patient, hospital=hospital)
        data.comment = comment
        data.disease.diseasetype = diseasetype
        data.disease.data = medicaldata
        data.date_time = timezone.now()
        data.save()
    return render(request, "profile_view.html", {"user": user})


def filter_hospital(request):
    if request.method == "GET":
        pass
    else:
        pass
    return render(request, 'filter.html')
        # pin_filter = None
        # cost_filter = None
        # name_filter = None
        # speciality_filter = None
        # star_filter = None
        # staff_strength_filter = None
def search_hosp(request):
    try:
        if request.method=='POST':
            srch=request.POST['srh']
            if srch:
                match=Hospital.objects.filter(Q(user__username__icontains=srch))
                if match:
                    print ("pass")
                    ur=match
                    return render(request,"allhospital.html",{"ur":ur})
        

        return render(request,"allhospital.html",{"ur":ur})

    except:
        return redirect("/hospital")
def hosp_profile(request,license):
    #one hospital cannot review another hospital
    try:
        hospital = models.Hospital.objects.get(license=license)
        hospitaldetails=models.HospitalDetails.objects.get(hospital=hospital)
    except (models.Hospital.DoesNotExist, models.HospitalDetails.DoesNotExist) :
        return  redirect("/hospital")
    if request.user.is_anonymous:
        review = None
    else:
        try:
            patient = models.Patient.objects.get(user = request.user)
            hospital = models.Hospital.objects.get(license=license)
            hospitaldetails=models.HospitalDetails.objects.get(hospital=hospital)
        except (models.Patient.DoesNotExist, models.Hospital.DoesNotExist, models.HospitalDetails.DoesNotExist) :
            return  redirect("/hospital")

    #Also get the review if exists
        review = models.Reviews.objects.get_or_create(hospital=hospital,patient=patient)[0]
        if request.method == "POST":
            reviewText = request.POST["review_text"]
            review.review = reviewText
            review.date_time = timezone.now()
            review.save();


    return render(request, "viewhospital.html", {"hosp": hospitaldetails,"review":review})

def search(request):

    return render(request,'find.html')

