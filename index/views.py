import email
from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from matplotlib.style import context, use
from plumbum import local
from .models import *
from django.core.mail import message, send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.files import File
import random
import http
import requests
import pyrebase
from datetime import datetime
from time import time
from joblib import load
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import string
import js2py
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder 
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split


# status conditions for the complaints
# 1) NotApproved - hiredby=solvedby="none" & orgreq!="none"
# 2) Solved - hiredby="none" & solvedby=orgreq=organization_name
# 3) Current/Running  - hiredby=organization_name, solvedby="none"
# 4) NotApproached - hiredby=solvedby=orgreq="none"

config={
    "apiKey": "AIzaSyBUFdq8lsezmB7qblDTmsluCt-TmE_QgaE",
    "authDomain": "femzo-4ea32.firebaseapp.com",
    "projectId": "femzo-4ea32",
    "storageBucket": "femzo-4ea32.appspot.com",
    "messagingSenderId": "801029656819",
    "appId": "1:801029656819:web:fcdd71ea3c023eece72786",
    "databaseURL": "https://femzo-4ea32-default-rtdb.firebaseio.com"
}
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
db=firebase.database()
fbstorage=firebase.storage()


def home(request):
    na=0
    cu=0
    sd=0
    total=0
    comps=dict(db.child("filecomplaint").get().val())
    
    for i in comps.keys():
        obj=comps[i]
        for i in obj.keys():
            obj1=dict(obj[i])
            if obj1['status']=="notapproached":
                na+=1
            if obj1['status']=="current":
                cu+=1
            if obj1['status']=="solved":
                sd+=1
            total+=1
    context={
        'total':total,
        'current':cu,
        'notapproached':na,
        'solved':sd,
    }
    try:
        localid=dict(authe.get_account_info(str(request.session['uid'])))['users'][0]['localId']
        if str(request.session['role'])=="organization":
            context['org']="org"
            username=db.child("organizations").child(str(localid)).child("name").get().val()
        else:
            context['gen']="gen"
            username=db.child("users").child(str(localid)).child("name").get().val()
        context['username']=username
    except:
        return redirect('loginpage')
    return render(request,'index.html',context)


def contactus(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        mssg=request.POST['mssg']
        db.child("ContactUs").push({"name":name,"Email":email,"Subject":subject,"Message":mssg})
    return redirect("home")
        


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
locmssg="StreetNumber15,Putlibowli,GowligudaChaman,Hyderabad,Telangana.Pin-500012(India)"
def filecomplaintform(request):
    try:
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        orgs=[]
        for i in db.child("organizations").get().each():
            orgs.append(dict(i.val())['name'])
    except:
        return redirect('loginpage')
    if request.method == 'POST':
        context = {
            'id':request.FILES.get('id'),
            'image':request.FILES.get('image'),
            'vedio':request.FILES.get('vedio'),

            'firstName':request.POST.get('firstName'),
            'lastName':request.POST.get('lastName'),
            'contactNo':request.POST.get('contactNo'),
            'email':request.POST.get('email'),
            'location':request.POST.get('location'),
            'subject':request.POST.get('subject'),
            'idno':request.POST.get('idno'),
            'message':request.POST.get('message'),
            'gen':request.POST.get('Gender'),
            'orgreq':request.POST.get('org'),
            'status':"unsolved",
            "solvedby":"none",
            'cid':"CID"+str(int(time()*1000))+"FEMZO"
        }
        context1={
            'firstName':request.POST.get('firstName'),
            'lastName':request.POST.get('lastName'),
            'contactNo':request.POST.get('contactNo'),
            'email':request.POST.get('email'),
            'location':request.POST.get('location'),
            'subject':request.POST.get('subject'),
            'idno':request.POST.get('idno'),
            'message':request.POST.get('message'),
            'gen':request.POST.get('Gender'),
            'orgreq':request.POST.get('org'),
            'status':"unsolved",
            "solvedby":"none",
            'cid':"CID"+str(int(time()*1000))+"FEMZO"
        }
        if str(context['orgreq'])!="none":
            context['hiredby']=context['orgreq']
        else:
            context['hiredby']="none"
        try:
            localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
            db.child("filecomplaint").child(localid).child(str(context1['cid'])).set(context1)
            if context['image'] is not None:
                fbstorage.child("filecomplaint").child(str(localid)).child(str(context1['cid'])).child("image").put(context['image'])
            if context['id'] is not None:
                fbstorage.child("filecomplaint").child(str(localid)).child(str(context1['cid'])).child("pdf").put(context['id'])
            if context['vedio'] is not None:
                fbstorage.child("filecomplaint").child(str(localid)).child(str(context1['cid'])).child("vedio").put(context['vedio'])
        except:
            return redirect('loginpage')
        
        e=EmailMessage('complaint filed successfully!',
            'Your form was submitted successfully, our organization will reach to ASAP. Kindly be patience. Thank you for using our website. -- team FEMZO ',
            settings.EMAIL_HOST_USER,
            [str(context1['email'])]
        )
        e.content_subtype='html'
        temp=get_template('responses.html')
        html=temp.render(context)
        res=BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), res)
        pdf = res.getvalue()
        filename = 'Responses_' + context1['firstName'] + '.pdf'
        e.attach(filename,pdf,'application/pdf')
        e.attach(context['id'].name,context['id'].read(),context['id'].content_type)
        e.attach(context['vedio'].name,context['vedio'].read(),context['vedio'].content_type)
        e.attach(context['image'].name,context['image'].read(),context['image'].content_type)
        e.send()
        return redirect("filecomplaintform")
    return render(request,'filecomplaint.html',{"orgs":orgs})

def logoutUser(request):
    auth.logout(request)
    return redirect('home')

def responses(request):
    return render(request,"responses.html")


def search_psdetails(request):
    if request.method=="POST":
        name=request.POST.get("name")
        address=request.POST.get("address")
        if(name=='' and address==''):
            return redirect("search")
        elif(name==''):
            obj=policeDetails.objects.filter(address=address)
        elif(address==''):
            obj=policeDetails.objects.filter(sname=name)
        else:
            obj=policeDetails.objects.filter(sname=name,address=address)
        context={'count':obj}
        return render(request,"policedetails.html",context)
    return render(request,"policedetails.html")
def view_psdetails(request):
    lst=(policeDetails.objects.all())
    context={'count':lst}
    return render(request,"policedetails.html",context)
def reset_psdetails(request):
    return redirect("/")
def policedetails(request):
    flag=False
    if request.user=='admin':
        flag=True
    return render(request,"policedetails.html",{'flag':flag})
def tactics(request):
    return render(request,"tactics.html")



def send_otp(mobile , otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    API_KEY_2="KSpx2bs07FghRPGtYV31BZIdarzLCDejwN8k5EAcXQHluWOTvMEfeK7CcQpAXgV94YT8ko5bwPZLHnqa"
    API_KEY="D5QuRUJr9olOekc6ZsI407BXn1HAxWiCPKSzbfp8q3VFwYvTgdl9VSZ0X4fpkKixGuDLMT7mrU5C3Pd6"
    otpmssg="Femzo Services: Your otp is "+str(otp)
    phnum=str(mobile)
    payload = "message="+otpmssg+"&language=english&route=q&numbers="+phnum
    headers = {
        'authorization': API_KEY,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return None

def login_attempt(request):
    if request.method == 'POST':
        memail = request.POST.get('email')
        mpassword = request.POST.get('password')
        try:
            user=authe.sign_in_with_email_and_password(memail,mpassword)
        except:
            return redirect('loginpage')
        request.session['uid']=str(user['idToken'])
        userrole=""
        if memail.lower()[-4:]==".org":
            userrole="organization"
        else:
            userrole="general"
        request.session['role']=userrole
        return redirect("home")
    return render(request,"login_page.html")
    
def register(request):
    if request.method == 'POST':
        memail = request.POST.get('email')
        pwd = request.POST.get('password')
        name = request.POST.get('name')
        phnum= request.POST.get('phnum')
        try:
            user=authe.create_user_with_email_and_password(memail,pwd)
            uid = user['localId']
            if memail.lower()[-4:]==".org":
                db.child("organizations").child(str(uid)).set({
                "name":name,
                "uemail":memail,
                "password":pwd,
                "phnum":phnum
                })
            else:
                db.child("users").child(str(uid)).set({
                "name":name,
                "uemail":memail,
                "password":pwd,
                "phnum":phnum
                })
            return redirect("loginpage")
        except:
            print("exeception")
            return render(request,'register.html')
    return render(request,'register.html')

def editprof(request):
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    if db.child("users").child(localid).get().val() is not None:
        details=dict(db.child("users").child(localid).get().val())
        context={"pdata":details}
    else:
        context={}
    return render(request,"edit_prof.html",context)
def dispprof(request):
    if request.session['role'] == "organization":
        return render(request,"orgaprofile.html")
    try:
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        if db.child("filecomplaint").child(str(localid)).get() is not None:
            comps=len(db.child("filecomplaint").child(str(localid)).get().each())

        if db.child("emergency_contacts").child(str(localid)).get() is not None:
            nums=[]
            for i in db.child("emergency_contacts").child(str(localid)).get().each():
                nums.append(i.val())
        else:
            nums={}
        if db.child("users").child(localid).get().val() is not None:
            details=dict(db.child("users").child(localid).get().val())
            context={"pdata":details,"nums":nums,"casesfiled":comps}
        else:
            context={"nums":nums}
    except:
        return redirect('loginpage')

    
    return render(request,"prof_index.html",context)

def updateDetails(request):
    if request.method=='POST':
        context={
            "name":str(request.POST.get("name")),
            "phnum":str(request.POST.get("phnum")),
            "address":str(request.POST.get("address")),
            "postcode":str(request.POST.get("postcode")),
            "state":str(request.POST.get("state")),
            "country":str(request.POST.get("country")),
            "profession":str(request.POST.get("profession")),
            "uemail":str(request.POST.get("email")),
        }
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        db.child("users").child(localid).set(context)
        return redirect('editprof')
    return redirect('editprof')

def addEmergencyContacts(request):
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    if request.method=='POST':
        context={
            "name":str(request.POST.get("name")),
            "phnum":str(request.POST.get("phnum")),
        }
        db.child("emergency_contacts").child(str(localid)).push(context)
    if db.child("emergency_contacts").child(str(localid)).get() is not None:
        nums=[]
        for i in db.child("emergency_contacts").child(str(localid)).get().each():
            nums.append(i.val())
    else:
        nums={}
    return render(request,"emergencynums.html",{"nums":nums})

def orgaprofile(request):
    context={}
    try:
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        pdata=dict(db.child("organizations").child(str(localid)).get().val())
        context={"pdata":pdata}
    except:
        pass
    return render(request,"orgaprofile.html",context)
def orgeditprofile(request):
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    pdata=dict(db.child("organizations").child(localid).get().val())
    if request.method=='POST':
        context={
            "name":str(request.POST.get("name")),
            "phnum":str(request.POST.get("phnum")),
            "mobnum":str(request.POST.get("mobnum")),
            "address":str(request.POST.get("address")),
            "uemail":str(request.POST.get("email")),
        }
        db.child("organizations").child(localid).set(context)
        pdata=dict(db.child("organizations").child(str(localid)).get().val())
    context={"pdata":pdata}
    return render(request,"orgeditprofile.html",context)
def orgdashboard(request):
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    notapproached=[]
    solved=[]
    current=[]
    approached=[]
    username=db.child("organizations").child(str(localid)).child("name").get().val()
    for i in (db.child("filecomplaint").get()).each():
        obj1=dict(i.val())
        for j in obj1.keys():
            obj2=dict(obj1[j])
            if obj2['status']=="solved" and obj2['orgreq']==str(username) and obj2['solvedby']==str(username) and obj2['hiredby']=="none":
                solved.append(obj2)
            if obj2['status']=="current" and obj2['hiredby']==str(username) and obj2['solvedby']=="none":
                current.append(obj2)
            if obj2['status']=="unsolved" and obj2['orgreq']==str(username) and obj2['hiredby']=="none" and obj2['solvedby']=="none":
                approached.append(obj2)
            if obj2['status']=="unsolved" and obj2['hiredby']=="none" and obj2['solvedby']=="none" and obj2['orgreq']=="none":
                notapproached.append(obj2)
            
    context={"notapproached":notapproached,"solved":solved,"current":current,"approached":approached}
    return render(request,"orgdashboard.html",context)


def viewcomplaints(request):
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    comps=[]
    for i in db.child("filecomplaint").child(str(localid)).get().each():
        comps.append(dict(i.val()))
    context={"comps":comps}
    return render(request,"viewcomplaints.html",context)

def displayComplaint(request,cid):
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    c={}
    for i in db.child("filecomplaint").child(str(localid)).get().each():
        if dict(i.val())['cid']==str(cid):
            c=dict(i.val())
    data={}
    mimg=fbstorage.child("filecomplaint").child(str(localid)).child(str(cid)).child("image").get_url(localid)
    mvid=fbstorage.child("filecomplaint").child(str(localid)).child(str(cid)).child("vedio").get_url(localid)
    mpdf=fbstorage.child("filecomplaint").child(str(localid)).child(str(cid)).child("pdf").get_url(localid)
    data["img"]=mimg
    data["vid"]=mvid
    data["pdf"]=mpdf
    context={"c":c,"data":data}
    try:
        uploadedfiles=[]
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        filename=dict(db.child("fromclient").child(str(cid)).get().val())
        filenames=[]
        publishdate=[]
        for i in filename.keys():
            filenames.append(filename[i]['filename'])
            publishdate.append(str(filename[i]['publishdate']))
        docs=[]
        
        for i in filenames:
            docs.append(str(fbstorage.child("fromclient").child(str(cid)).child(str(i)).get_url(str(localid))))
        for i in range(len(docs)):
            uploadedfiles.append({"name":filenames[i],"path":docs[i],"publishdate":publishdate[i]})
        context['myuploadedfiles']=uploadedfiles
    except:
        pass
    try:
        uploadedfiles=[]
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        filename=dict(db.child("fromorganization").child(str(cid)).get().val())
        filenames=[]
        publishdate=[]
        for i in filename.keys():
            filenames.append(filename[i]['filename'])
            publishdate.append(str(filename[i]['publishdate']))
        docs=[]
        for i in filenames:
            docs.append(str(fbstorage.child("fromorganization").child(str(cid)).child(str(i)).get_url(str(localid))))
        for i in range(len(docs)):
            uploadedfiles.append({"name":filenames[i],"path":docs[i],"publishdate":publishdate[i]})
        context['uploadedfiles']=uploadedfiles
    except:
        pass
    return render(request,"displayComplaint.html",context)

def orgdispcomp(request,cid):
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    c={}
    obj1=dict(db.child("filecomplaint").get().val())
    for i in obj1.keys():
        obj2=dict(obj1[i])
        for j in obj2.keys():
            if obj2[j]['cid']==str(cid):
                c=obj2[j]
    context={"c":c}
    obj=dict(db.child("filecomplaint").get().val())
    for i in obj.keys():
        obj1=dict(obj[i])
        for j in obj1.keys():
            if str(j)==str(cid):
                locid=str(i)
    if locid:
        data={}
        try:
            mimg=fbstorage.child("filecomplaint").child(locid).child(str(cid)).child("image").get_url(locid)
            data["img"]=mimg
        except:
            pass
        try:
            mvid=fbstorage.child("filecomplaint").child(locid).child(str(cid)).child("vedio").get_url(locid)
            data["vid"]=mvid
        except:
            pass
        mpdf=fbstorage.child("filecomplaint").child(locid).child(str(cid)).child("pdf").get_url(locid)
        data["pdf"]=mpdf
        context={"c":c,"data":data}
    
    try:
        uploadedfiles=[]
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        filename=dict(db.child("fromorganization").child(str(cid)).get().val())
        filenames=[]
        publishdate=[]
        
        for i in filename.keys():
            filenames.append(filename[i]['filename'])
            publishdate.append(str(filename[i]['publishdate']))
        docs=[]
        for i in filenames:
            docs.append(str(fbstorage.child("fromorganization").child(str(cid)).child(str(i)).get_url(str(localid))))
        for i in range(len(docs)):
            uploadedfiles.append({"name":filenames[i],"path":docs[i],"publishdate":publishdate[i]})
        context['uploadedfiles']=uploadedfiles
    except:
        pass
    try:
        uploadedfiles=[]
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        filename=dict(db.child("fromclient").child(str(cid)).get().val())
        filenames=[]
        publishdate=[]
        for i in filename.keys():
            filenames.append(filename[i]['filename'])
            publishdate.append(str(filename[i]['publishdate']))
        docs=[]
        for i in filenames:
            docs.append(str(fbstorage.child("fromclient").child(str(cid)).child(str(i)).get_url(str(localid))))
        for i in range(len(docs)):
            uploadedfiles.append({"name":filenames[i],"path":docs[i],"publishdate":publishdate[i]})
        context['clientuploadedfiles']=uploadedfiles
    except:
        pass
    return render(request,"orgdispcomp.html",context)


def nasolvednaclicked(request,cid):
    obj=dict(db.child("filecomplaint").get().val())
    for i in obj.keys():
        obj1=dict(obj[i])
        for j in obj1.keys():
            if str(j)==str(cid):
                locid=str(i)
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    username=str(db.child("organizations").child(str(localid)).child("name").get().val())
    db.child("filecomplaint").child(locid).child(str(cid)).update({"hiredby":username,"orgreq":username,"solvedby":"none","status":"current"})
    return redirect("orgdashboard")

def currentclicked(request,cid):
    obj=dict(db.child("filecomplaint").get().val())
    for i in obj.keys():
        obj1=dict(obj[i])
        for j in obj1.keys():
            if str(j)==str(cid):
                locid=str(i)
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    username=str(db.child("organizations").child(str(localid)).child("name").get().val())
    db.child("filecomplaint").child(locid).child(str(cid)).update({"hiredby":"none","orgreq":username,"solvedby":username,"status":"solved"})
    return redirect("orgdashboard")

def orgsubmitdoc(request,cid):
    if request.method=="POST":
        docname=str(request.POST.get("filename"))
        mdoc=request.FILES.get("compdoc")
        localid=str(dict(authe.get_account_info(request.session['uid']))['users'][0]['localId'])
        username=str(db.child("organizations").child(str(localid)).child("name").get().val())
        fbstorage.child("fromorganization").child(str(cid)).child(str(docname)).put(mdoc)
        publishdate=str(datetime.now())[:-7]
        db.child("fromorganization").child(str(cid)).push({"orgname":username,"filename":docname,"publishdate":publishdate})
    return redirect("orgdispcomp",cid)

def compsubmitdoc(request,cid):
    if request.method=="POST":
        docname=str(request.POST.get("filename"))
        mdoc=request.FILES.get("compdoc")
        fbstorage.child("fromclient").child(str(cid)).child(str(docname)).put(mdoc)
        publishdate=str(datetime.now())[:-7]
        db.child("fromclient").child(str(cid)).push({"filename":docname,"publishdate":publishdate})
    return redirect("displayComplaint",cid)



def chatwithorgs(request):
    context={}
    obj=dict(db.child("organizations").get().val())
    orgs=[]
    for i in obj.keys():
        obj1=dict(obj[i])
        orgs.append({"name":obj1['name'],"email":obj1['uemail']})
    context['orgs']=orgs
    try:
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        chatid=str(request.session['chatid'])
        obj1=dict(db.child("chatrooms").child(chatid).get().val())
        lst=[]
        for i in obj1.keys():
            obj2=dict(obj1[i])
            lst.append(obj2)
        context['conversations']=lst
        context['orgname']=str(request.session['orgname'])
    except:
        pass
    return render(request,"chatwithorgs.html",context)

def initiateChat(request):
    if request.method=="POST":
        orgname=str(request.POST.get("selectedorg"))
        if orgname=="":
            return redirect("chatwithorgs")
        localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
        chatid=orgname+str(localid)
        request.session['orgname']=orgname
        request.session['chatid']=chatid
        flag=True
        try: 
            print(len(dict(db.child("chatrooms").child(str(chatid)).get().val())))
            flag=False
        except:
            pass
        if flag:
            db.child("chatrooms").child(str(chatid)).push({"org":"yes","mess":"Hello! How Can we help you","timestamp":str(datetime.now())[:-7]})
            db.child("chatrooms").child(str(chatid)).push({"mess":"Hello!","timestamp":str(datetime.now())[:-7]})
    return redirect("chatwithorgs")

def sendMsg(request):
    if request.method=="POST":
        mssg=str(request.POST.get("mssg"))
        if mssg != "":
            chatid=str(request.session['chatid'])
            db.child("chatrooms").child(str(chatid)).push({"mess":mssg,"timestamp":str(datetime.now())[:-7]})
    return redirect("chatwithorgs")

def myConversations(request):
    context={}
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    strname=str(db.child("organizations").child(str(localid)).child("name").get().val())
    try:
        lst=[]
        for i in db.child("chatrooms").get().val():
            org=str(i)[:len(strname)]
            gen=str(i)[len(strname):]
            print(gen)
            if org==strname:
                username=db.child("users").child(str(gen)).child("name").get().val()
                lst.append({"genusername":str(username),"chatid":str(i)})
        context['chatrooms']=lst
    except:
        pass
    return render(request,"chatwithusers.html",context)

def viewchatwithuser(request,chatid):
    context={}
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    strname=str(db.child("organizations").child(str(localid)).child("name").get().val())
    org=str(chatid)[:len(strname)]
    gen=str(chatid)[len(strname):]
    username=db.child("users").child(str(gen)).child("name").get().val()
    context['genusername']=str(username)
    conversations=[]
    obj=dict(db.child("chatrooms").child(str(chatid)).get().val())
    for i in obj.keys():
        conversations.append(dict(obj[i]))
    context['conversations']=conversations
    context['chatid']=str(chatid)
    return render(request,"viewchatwithuser.html",context)

def sendMsgtoclient(request,chatid):
    if request.method=="POST":
        mssg=str(request.POST.get("mssg"))
        if mssg != "":
            db.child("chatrooms").child(str(chatid)).push({"org":"yes","mess":mssg,"timestamp":str(datetime.now())[:-7]})
    return redirect("viewchatwithuser",chatid)
def deleteConv(request,chatid):
    db.child("chatrooms").child(str(chatid)).remove()
    return redirect("myConversations")


def generateSummary(request,cid):
    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    compdetails=dict(db.child("filecomplaint").child(str(localid)).child(str(cid)).get().val())
    mpdf=fbstorage.child("filecomplaint").child(localid).child(str(cid)).child("pdf").get_url(localid)
    mimg=fbstorage.child("filecomplaint").child(localid).child(str(cid)).child("image").get_url(localid)
    mvid=fbstorage.child("filecomplaint").child(localid).child(str(cid)).child("vedio").get_url(localid)
    compdetails['pdf']=mpdf
    compdetails['img']=mimg
    compdetails['vid']=mvid
    template_path = 'summary.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Femzo_Complaint_Summary.pdf"'
    template = get_template(template_path)
    html = template.render(compdetails)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sendCurrLoc(request):
    url = "https://www.fast2sms.com/dev/bulkV2"
    #API_KEY="KSpx2bs07FghRPGtYV31BZIdarzLCDejwN8k5EAcXQHluWOTvMEfeK7CcQpAXgV94YT8ko5bwPZLHnqa"
    #API_KEY="D5QuRUJr9olOekc6ZsI407BXn1HAxWiCPKSzbfp8q3VFwYvTgdl9VSZ0X4fpkKixGuDLMT7mrU5C3Pd6"
    API_KEY="rSP3IYb0JLQlNsmVinRKWqBhy95Gxt6foFXUvjucek18aAwpTHMw7kFdI51RJyUv0tlNEirps3Ce69jo"

    localid=dict(authe.get_account_info(request.session['uid']))['users'][0]['localId']
    obj=dict(db.child("emergency_contacts").child(str(localid)).get().val())
    phnums=""
    for i in obj.keys():
        obj1=dict(obj[i])
        phnums+=obj1['phnum']+","
    phnums=phnums[:len(phnums)-1]
    print(phnums)
    print(locmssg)
    payload = locmssg+"&language=english&route=q&numbers="+phnums
    print(payload)
    headers = {
        'authorization': API_KEY,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

    return redirect("home")







dataset=pd.read_csv('C:/Users/cheraka/Desktop/WebDev/project_femzo/Notebooks/safeornot2.csv')
dataset.rename(columns = {'People.Frequency':'People_Frequency'}, inplace = True)
df=dataset.copy()

def safeplacepredict(request):
    if request.method=='POST':
        x=df.iloc[:,:-1].values
        y=df.iloc[:,-1].values
        Area=request.POST['textlocn']
        Zone=request.POST['textZone']
        Time=request.POST['menu_time']
        People_Frequency=request.POST['freq']
        characters = ['Yes','No']
        Police_Station = ''.join(random.choice(characters) for i in range(1))
        characters = ['Yes','No']
        Is_Bar = ''.join(random.choice(characters) for i in range(1))
        characters = ['Middle','Outer']
        Tier = ''.join(random.choice(characters) for i in range(1))
        characters = ['Low','Middle','High']
        Residence_Level    = ''.join(random.choice(characters) for i in range(1))
        sample=np.array([[Area,	Zone	,Time,	People_Frequency,	Police_Station,	Is_Bar,	Tier	,Residence_Level]])
        sample1=np.append(x,sample,0)
       
        for i in range(8):
            ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [-1])],remainder='passthrough')
            sample1 = np.array(ct.fit_transform(sample1))
            x = np.array(ct.fit_transform(x))
        t=sample1[-1]
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=0)
        
        classifier=SVC(kernel='rbf', random_state=0)
        classifier.fit(x_train,y_train)
        y_pred = classifier.predict([t])
        print(y_pred)

        return render(request,'safeplacepredict.html',{'result':y_pred[0]})
    return render(request,'safeplacepredict.html')

