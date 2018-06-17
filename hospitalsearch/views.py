from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from hospital.models import Hospital
from django.db.models import Q


# Create your views here.

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

def search(request):
    if request.method=='POST':
        srch=request.POST['srh']
        if srch:
            match=Hospital.objects.filter(Q(user__username__icontains=srch))
            if match:
                print ("hello")
                return render(request,'find.html')
    return render(request,'find.html')
