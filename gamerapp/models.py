from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class games(models.Model):
    gamename = models.CharField(max_length=20)
    gamedetail = models.TextField
    genre = models.CharField(max_length=30)

    def __str__(self):
        return self.gamename


class UserRegistration(models.Model):
    USER_TYPE_CHOICES = [
        ('user', 'user'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='user')
    password = models.CharField(max_length=255)  # Store hashed passwords

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()  # Changed to TextField for longer summaries
    genre = models.CharField(max_length=100, default="action")
    image = models.ImageField(upload_to='game_images/')  # Adjust the path as necessary
    available_devices = models.CharField(max_length=255, default="pc")

    # Pricing structure (assuming different stores have different pricing)
    pricing = models.JSONField(default=dict)  # Use JSONField to store pricing details for different platforms

    def __str__(self):
        return self.title


class RequiredSpecs(models.Model):
    game = models.OneToOneField('Game', on_delete=models.CASCADE, related_name='required_specs')  # Use string reference
    processor = models.CharField(max_length=100)
    ram = models.PositiveIntegerField()  # Use PositiveIntegerField for RAM in GB
    gpu = models.CharField(max_length=100)
    storage = models.PositiveIntegerField()  # Storage in GB


class CurrentSpecs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cpu = models.CharField(max_length=255, default='Unknown')  # Default value for existing rows
    ram = models.FloatField(default=0)  # Default value for existing rows
    storage = models.FloatField(default=0)  # Default value for existing rows
    os_version = models.CharField(max_length=255, default='Unknown')  # Default value for existing rows
    gpu = models.CharField(max_length=255, default='Unknown')  # Default value for existing rows
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Specs"


class Tournament(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    available_tournaments = models.IntegerField()
    image = models.ImageField(upload_to='tournaments/')
    name = models.CharField(max_length=255, null=False, default='Default Tournament')

    def __str__(self):
        return self.title


class UpcomingGame(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    platform = models.CharField(max_length=100)
    website_url = models.URLField()
    image = models.ImageField(upload_to='upcoming_games/')

    def __str__(self):
        return self.title


class RegisteredEvents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_events')
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    game_title = models.CharField(max_length=255)  # New field for the game title
    platform = models.CharField(max_length=100)  # New field for the gaming platform
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} - {self.user.username} ({self.game_title})"


class Event(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    # Additional fields as needed.
    def __str__(self):
        return self.name

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')