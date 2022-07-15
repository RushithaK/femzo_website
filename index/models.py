import email
from operator import mod
from django.core.checks import messages
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.contrib.auth.models import User
from regex import F
from requests import request

class policeDetails(models.Model):
    sname=models.CharField(max_length=30)
    address=models.CharField(max_length=100)
    psemail=models.EmailField()
    psnumber=models.IntegerField()
    def __str__(self):
        return self.sname
# class contactusmodel(models.Model):
#     name=models.CharField(max_length=20)
#     email=models.EmailField()
#     mssg=models.TextField()
#     subject=models.CharField(max_length=50)
#     def __str__(self) -> str:
#         return self.name+":"+self.subject

# class complaint(models.Model):
#     cid = models.AutoField(primary_key=True)
#     user_name = models.ForeignKey(User, on_delete=DO_NOTHING)
#     victims_fname = models.CharField(max_length=20)
#     victims_lname = models.CharField(max_length=20)
#     contact_no = models.IntegerField()
#     email = models.EmailField()
#     location = models.CharField(max_length=500)
#     subject = models.TextField(max_length=50)
#     idproof_number = models.CharField(max_length=30)
#     idprooof = models.FileField(upload_to='data/id/')
#     vedio = models.FileField(upload_to='data/vids/')
#     image = models.FileField(upload_to='data/imgs/')
#     message = models.TextField(max_length=50)
#     gender=models.CharField(max_length=50,default='NA',null=True)
#     def __str__(self) -> str:
#         return str(self.cid)+') '+self.victims_fname+' '+self.victims_lname+' <- '+str(self.user_name)
    


# class Profile(models.Model):
#     user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     email=models.EmailField(default="")
#     mobile = models.CharField(max_length=20)
#     otp = models.CharField(max_length=6)
#     def __str__(self) -> str:
#         return self.mobile

# class ProfileDetails(models.Model):
#     user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     fname= models.CharField(max_length=20,default="",null=False)
#     lname= models.CharField(max_length=20,null=False,default="")
#     phnumber= models.CharField(max_length=10,null=False)
#     address= models.CharField(max_length=50,null=False,default="")
#     postcode= models.CharField(max_length=10,null=False,default="")
#     state= models.CharField(max_length=20,default="")
#     country= models.CharField(max_length=20,default="")
#     profession= models.CharField(max_length=30,default="")
#     uemail= models.EmailField(null=False,default="")
#     def __str__(self) -> str:
#         return self.fname


# class EmergencyContacts(models.Model):
#     user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     phnumber=models.CharField(max_length=10,null=False,default="")
#     holdersname=models.CharField(max_length=10,null=False,default="")
#     def __str__(self) -> str:
#         return self.user.username 


