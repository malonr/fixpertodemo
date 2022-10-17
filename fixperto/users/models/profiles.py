"""Profile model."""
from django.db import models
from utils import FixpertoModel
from django.core.validators import RegexValidator
from datetime import date

def get_default_last_login():
    today = date.today()
    last_login = today.strftime("%B %d, %Y")
    print (last_login)


class Profile(FixpertoModel):
    """Profile model.
    A profile holds a user's public data like  name, last name,
    email, phone number, birthdate
    """
    
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    
    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    birthdate = models.DateField(null=True)
    
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    last_login = models.DateTimeField(default= get_default_last_login)
    #last_entry = models.DateTimeField() 
    
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
       
    def __str__(self):
        return str(self.user)
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def name(self):
        return self.user.name
    
    @property
    def last_name(self):
        return self.user.last_name
    
    