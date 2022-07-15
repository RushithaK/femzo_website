from django.urls import path
from .views import *

urlpatterns = [


    path('responses/',responses,name='responses'),
    path("search/",search_psdetails,name="search"),
    path("view/",view_psdetails,name="view"),
    path("reset/",reset_psdetails,name="reset"),
    path("policedetails/",policedetails,name="policedetails"),

    path('',home,name='home'),
    path('filecomplaintform/',filecomplaintform,name='filecomplaintform'),
    path('logoutUser/',logoutUser,name='logoutUser'),
    path('contactus/',contactus,name='contactus'),
    path("tactics/",tactics,name="tactics"),
    path("loginpage/", login_attempt , name="loginpage"),
    path("register/" , register , name="register"),
    path("editprof/",editprof,name="editprof"),
    path("dispprof/",dispprof,name="dispprof"),
    path("updateDetails/",updateDetails,name="updateDetails"),
    path("addEmergencyContacts/",addEmergencyContacts,name="addEmergencyContacts"),
    path("orgeditprofile/",orgeditprofile,name="orgeditprofile"),
    path("orgaprofile/",orgaprofile,name="orgaprofile"),
    path("orgdashboard/",orgdashboard,name="orgdashboard"),
    path("viewcomplaints/",viewcomplaints,name="viewcomplaints"),
    path("displayComplaint/<cid>/",displayComplaint,name="displayComplaint"),
    path("orgdispcomp/<cid>/",orgdispcomp,name="orgdispcomp"),
    path("nasolvednaclicked/<cid>/",nasolvednaclicked,name="nasolvednaclicked"),
    path("currentclicked/<cid>/",currentclicked,name="currentclicked"),
    path("orgsubmitdoc/<cid>/",orgsubmitdoc,name="orgsubmitdoc"),
    path("compsubmitdoc/<cid>/",compsubmitdoc,name="compsubmitdoc"),

    path("chatwithorgs/",chatwithorgs,name="chatwithorgs"),
    path("initiateChat/",initiateChat,name="initiateChat"),
    path("safeplacepredict/",safeplacepredict,name="safeplacepredict"),
    path("sendMsg/",sendMsg,name="sendMsg"),
    path("myConversations/",myConversations,name="myConversations"),
    path("viewchatwithuser/<chatid>/",viewchatwithuser,name="viewchatwithuser"),
    path("sendMsgtoclient/<chatid>/",sendMsgtoclient,name="sendMsgtoclient"),
    path("deleteConv/<chatid>/",deleteConv,name="deleteConv"),


    path("generateSummary/<cid>/",generateSummary,name="generateSummary"),


    path("sendCurrLoc/",sendCurrLoc,name="sendCurrLoc"),
]
