from django.shortcuts import render,HttpResponse,redirect
from django.http import StreamingHttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import base64,time,json
from django.views.decorators.csrf import csrf_exempt
from .models import MsgHistory
from django.contrib.auth.models import User

# Create your views here.

def chat(request):
    if request.user.is_authenticated:
        res=render(request,"chat.html",{"myuser":request.user.username})
        request.session["nowdata"]=MsgHistory.objects.all().count()
        return res
    if len(str(base64.b64decode(str(request.META.get("HTTP_AUTHORIZATION")).split(" ")[-1])).split(':'))!=1:
        username,password=str(base64.b64decode(str(request.META.get("HTTP_AUTHORIZATION")).split(" ")[-1]).decode()).split(':')
        print(username,password)
        user_obj = auth.authenticate(username=username,password=password)
        if user_obj:
            res=render(request,"chat.html",{"myuser":username})
            request.session["nowdata"]=MsgHistory.objects.all().count()
            auth.login(request,user_obj)
            return res
    resp=HttpResponse('Unauthorized',status=401)
    resp["WWW-Authenticate"]='Basic realm=\"Access to the staging site\", charset=\"UTF-8\"'
    return resp

def logout(request):
    auth.logout(request)
    resp=HttpResponse('Unauthorized',status=401)
    resp["WWW-Authenticate"]='Basic realm=\"Access to the staging site\", charset=\"UTF-8\"'
    return resp

def getnewmsg(request):
    ostream=""
    tt=MsgHistory.objects.all().count()
    nowdata=int(request.session.get("nowdata"))
    if tt>nowdata:
        nowdata=nowdata+1
        request.session["nowdata"]=nowdata+1
        obj=MsgHistory.objects.get(id=nowdata)
        ostream=ostream+'data: {}\n\n'.format(json.dumps({
            "id":nowdata,
            "msgs":obj.msgs,
            "foruser":obj.foruser.username,
            "crtime":obj.crtime.strftime("%Y/%m/%e %H:%M:%S"),
        }))
    res=HttpResponse(ostream,content_type='text/event-stream')
    return res

@csrf_exempt
def putnewmsg(request):
    if request.user.is_authenticated:
        MsgHistory.objects.create(foruser=User.objects.get(username=request.user.username),msgs=request.POST.get("msgs"))
        return HttpResponse("")
    else:
        return HttpResponse("")