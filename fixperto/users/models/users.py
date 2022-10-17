from pyexpat import model
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from utils import FixpertoModel

class  User(FixpertoModel, AbstractBaseUser):
    """User model.
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """
    email = models.EmailField(
        max_length = 255,
        unique = True,
        error_messages={"unique": "A user with that email already exists."},
        )
    name = models.CharField( max_length = 255, blank = True, null = True)
    last_name = models.CharField(max_length = 255, blank = True, null = True)
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ) )
    
    is_client = models.BooleanField(default = False)
    is_expert = models.BooleanField(default = False)
    is_agent = models.BooleanField(default = False)
    
    class Meta:
        """Meta class."""

        verbose_name = ("user")
        verbose_name_plural = ("users")
    
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']
    
    def __str__(self):
        return f'{self.name} {self.last_name}'
    
class Client(models.Model):
    user = models.OnetoOneField(User, related_name= "client", on_delete = models.CASCADE)

class Expert(models.Model):
    user = models.OnetoOneField(User, related_name= "expert", on_delete = models.CASCADE)

class Agent(models.Model):
        user = models.OnetoOneField(User, related_name= "expert", on_delete = models.CASCADE)

    
    
    


       