from django.db import models
from datetime import date

# Create your Manager models here
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        filteredResult = User.objects.filter(username = postData['username'])
        print(filteredResult)
        # name required
        if len(postData['name']) == 0:
            errors['nameReq'] = "Name is Required"
        elif len(postData['name']) < 3:
            errors['nameReq'] = "Name must be at least 3 characters"
        # username required
        if len(postData['username']) == 0:
            errors['usernameReq'] = "Username is Required"
        elif len(postData['username']) < 3:
            errors['usernameReq'] = "Username must be at least 3 characters"
        # check if username already exists in db
        if len(filteredResult) > 0:
            errors['usernametaken'] = "This Username is Taken"
        # pw required
        if len(postData['pw']) == 0:
            errors['pwReq'] = "Password is Required"
        elif len(postData['pw']) < 8:
            errors['pwReq'] = "Password must be at least 8 characters"
        # confirm pw required
        if postData['conpw'] != postData['pw']:
            errors['conpwReq'] = "Password does not match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        filteredResult = User.objects.filter(username = postData['usrnm'])
        if len(postData['usrnm']) == 0:
            errors['usrnmReq'] = "Username is Required"    
        elif len(filteredResult)==0:
            errors['nouserfound'] = "This User was not found. Please Register"
        else:
            print("user found!")
            if filteredResult[0].password != postData['psw']:
                errors['passwordmatch'] = "Incorrect Password"
        if len(postData['psw']) == 0:
            errors['pswReq'] = "Password is Required"
        return errors


class TravelManager(models.Manager):
    def itemValidator(self, postData):
        errors = {}
        today = date.today
        if len(postData['destin']) == 0:
            errors['destinlength'] = "Destination must not be empty"
        elif len(postData['destin']) < 3:
            errors['destinReq'] = "Destination must be at least 3 characters"   
        if len(postData['descrip']) == 0:
            errors['descriplength'] = "Description must not be empty"
        elif len(postData['descrip']) < 3:
            errors['descripReq'] = "Description must be at least 3 characters"
        if not postData['from']:
            errors["fromlen"] = "Start Date is required!"
        elif postData['from'] < str(today()):
            errors['fromwrong'] = "You trying to rewind time? Let me know!.."
        if not postData['to']:
        	errors['tolen'] = "End Date is required!"
        elif postData['to'] < postData['from']:
            errors['towrong'] = "You cannot return from a trip before it begins!..dummy"
        return errors


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    travel_start = models.DateField()
    travel_end = models.DateField()
    uploader = models.ForeignKey(User, related_name="travelUploader", on_delete = models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="travelFav")
    plan = models.CharField(max_length=255)
    objects = (TravelManager)()
