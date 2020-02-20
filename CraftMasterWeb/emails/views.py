from django.shortcuts import render, HttpResponse
from datetime import date
from .models import Email
import json
# Create your views here.
def getEmail(request):
    if request.method=="POST":
        email = request.POST.get('email')
        Email.objects.create(
            email = email,
            register_date = date.today(),
        )
        res = {'ret':0, 'msg':'ok'}
        return HttpResponse(json.dumps(res),content_type='application/json')
    return render(request,'index.html')
