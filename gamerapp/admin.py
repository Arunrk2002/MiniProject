from django.contrib import admin
from .models import Game,RequiredSpecs,UserRegistration,CurrentSpecs,Tournament, UpcomingGame,RegisteredEvents,Event, Registration
# Register your models here.

admin.site.register(Game)
admin.site.register(RequiredSpecs)
admin.site.register(UserRegistration)
admin.site.register(CurrentSpecs)
admin.site.register(Tournament)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(UpcomingGame)
admin.site.register(RegisteredEvents)