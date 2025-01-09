from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import os
import platform
import psutil
import cpuinfo
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserRegistration,Game
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login as auth_login
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Game, CurrentSpecs, RequiredSpecs
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Event, Registration

# Create your views here.
def index(request):
    game="Blackmyth_wukong"
    return render(request,'index.html',{'game': game})

#def home(request):
 #   return render(request,'home.html')
from .models import Tournament, UpcomingGame
def newsus(request):
    tournaments = Tournament.objects.all()
    upcoming_games = UpcomingGame.objects.all()
    return render(request,'newsus.html', {'tournaments': tournaments, 'upcoming_games': upcoming_games})

def log(request):
    return render(request,'login.html')
#
def spec(request):
    return render(request,'spec1.html')
def ind(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Try to authenticate the user
        user = authenticate(request, username=email.split('@')[0], password=password)  # Assuming username is based on the email

        if user is not None:
            # User is authenticated
            login(request, user)
            return redirect('indexus')  # Redirect to your home or dashboard page
        else:
            # Invalid credentials
            messages.error(request, "Invalid username or password.")
            return render(request, 'index.html')

    return render(request, 'index.html')

import GPUtil

 # Import GPUtil
# User registration view
from django.contrib.auth import login

def reg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate that passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register.html')

        # Create new user
        user = User.objects.create_user(username=email.split('@')[0],  # Create username from email (or use a different logic)
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        password=password)
        user.save()

        # Log in the user
        login(request, user)

        return redirect('indexus')  # Redirect to your home or dashboard page

    return render(request, 'registration.html')

def get_os_version():
    os_name = platform.system()  # Get the OS name (e.g., 'Windows')
    os_release = platform.release()  # Get the OS release version (e.g., '10', '11')

    # Map the OS release to a user-friendly name
    if os_name == "Windows":
        if os_release == "11":
            return "Windows 10"
        elif os_release == "10":
            return "Windows 11"
        else:
            return f"Windows {os_release}"  # For other versions
    return f"{os_name} {os_release}"  # For non-Windows OS


def get_pc_specs(request):
    try:
        # Get CPU information
        cpu_info = cpuinfo.get_cpu_info()
        specs = {
            'cpu': cpu_info['brand_raw'],
            'ram': round(psutil.virtual_memory().total / (1024. ** 3)+1),  # Total RAM in GB
            'storage': round(psutil.disk_usage('/').total / (1024. ** 3)),  # Total Storage in GB
            'os_version': get_os_version(),  # User-friendly OS version
        }

        # Get GPU information using GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:  # Check if GPUs are detected
            specs['gpu'] = ', '.join([gpu.name for gpu in gpus])  # List GPU names
        else:
            specs['gpu'] = 'No GPU detected'

        # Print the specs to the terminal
        print("PC Specs:", specs)

        return JsonResponse(specs)
    except Exception as e:
        print("Error fetching PC specs:", str(e))  # Log the error to the terminal
        return JsonResponse({'error': str(e)}, status=500)


def indexus(request):
    return render(request,'indexus.html')

#def newsus(request):
    #return render(request,'newsus.html')

def profile(request):

    return render(request,'profile.html')
def chatbot(request):
    return render(request,'chatbot.html')
def join(request):
    return render(request,'join.html')

def home(request):
    games=Game.objects.all()
    return render(request,'homeus.html',{'games':games})

from .models import Game, CurrentSpecs  # Make sure to import your models

def game_detail(request, game_id):
    # Fetch the game based on ID
    game = get_object_or_404(Game, id=game_id)

    # Fetch the required specs for the game
    required_specs = get_object_or_404(RequiredSpecs, game=game)

    current_specs = None
    if request.user.is_authenticated:  # Check if the user is authenticated
        # Fetch current specs for the authenticated user
        current_specs = CurrentSpecs.objects.filter(user=request.user).first()

    return render(request, 'games.html', {
        'game': game,
        'required_specs': required_specs,  # Add required specs to the context
        'current_specs': current_specs
    })
from .models import Game,RequiredSpecs,UserRegistration,CurrentSpecs
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  # Use this only for testing; it's safer to keep CSRF protection
def save_pc_specs(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Load JSON data
            print("Received data:", data)  # Log received data for debugging

            # Save specs with the data from the POST request
            specs = CurrentSpecs.objects.create(
                user=request.user,
                cpu=data.get('cpu', 'Unknown'),
                gpu=data.get('gpu', 'Unknown'),
                ram=data.get('ram', 0),
                storage=data.get('storage', 0),
                os_version=data.get('os_version', 'Unknown')
            )
            print("Specs saved:", specs)  # Log saved specs for debugging
            return JsonResponse({'message': 'Specs saved successfully!'}, status=201)
        except Exception as e:
            print("Error saving specs:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
import openai
openai.api_key = openai.api_key = "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"

def chat_with_bot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Send the user's message to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Get the response text from OpenAI
        bot_reply = response['choices'][0]['message']['content']

        return JsonResponse({'reply': bot_reply})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

from .models import games
def search(request):
    query = request.GET.get('q')  # Get the search query from the GET parameters
    results = []

    if query:
        results = games.objects.filter(gamename__icontains=query)  # Ensure you're searching using the correct field

    return render(request, 'search_results.html', {'results': results, 'query': query})  # Pass the query to the template

def logout_view(request):
    logout(request)
    return redirect('ind')
def profile(request):
    current_specs = None
    if request.user.is_authenticated:  # Check if the user is authenticated
        # Fetch current specs for the authenticated user
        current_specs = CurrentSpecs.objects.filter(user=request.user).first()


    """Render the profile view with user details."""
    return render(request, 'profile.html', {'user': request.user,'current_specs': current_specs})


def edit_profile(request):
    """Handle profile editing."""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        # Update the user instance
        user = request.user
        user.first_name, user.last_name = full_name.split(' ', 1)  # Split full name into first and last
        user.email = email
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return redirect('profile')

from .models import games
import random
from django.core.mail import send_mail
from django.conf import settings
def search(request):
    query = request.GET.get('q')  # Get the search query from the GET parameters
    results = []

    if query:
        results = games.objects.filter(gamename__icontains=query)  # Ensure you're searching using the correct field

    return render(request, 'search_results.html', {'results': results, 'query': query})  # Pass the query to the template
from django.urls import reverse

def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate OTP
            otp = random.randint(100000, 999999)
            # Store OTP and email in session
            request.session['otp'] = otp
            request.session['email'] = email
            # Send OTP via email
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            # Redirect to OTP verification page with query parameter
            url = f"{reverse('password_reset')}?step=verify"
            return redirect(url)
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
    return render(request, 'pass-reset.html', {'step': 'request'})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp = request.session.get('otp')
        if otp and int(entered_otp) == otp:
            # OTP is correct, redirect to set new password page with parameter
            return redirect(f"{reverse('set_new_password')}?step=set_password")
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'pass-reset.html', {'step': 'verify'})

def set_new_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        email = request.session.get('email')
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successful')
            # Clear the OTP and email from the session
            del request.session['otp']
            del request.session['email']
            return redirect('ind')
        except User.DoesNotExist:
            messages.error(request, 'An error occurred. Please try again.')
    return render(request, 'pass-reset.html', {'step': 'set_password'})


from .models import RegisteredEvents
def join(request):
    if request.user.is_authenticated:  # Check if the user is authenticated
        # Fetch current specs for the authenticated user
        event = Event.objects.all()
    return render(request,'join.html',{'user': request.user,'event': event})

# def register_event(request):
#     if request.method == 'POST':
#         event_name = request.POST.get('event_name')
#         event_date = request.POST.get('event_date')
#         game_title = request.POST.get('game_title')      # Get game title from form
#         platform = request.POST.get('platform')          # Get platform from form
#
#         # Validate input
#         if not event_name or not event_date or not game_title or not platform:
#             messages.error(request, 'Please provide all required fields.')
#             return redirect('register_event')  # Redirect back to registration page
#
#         # Create a new RegisteredEvents instance
#         registered_event = RegisteredEvents.objects.create(
#             user=request.user,
#             event_name=event_name,
#             event_date=event_date,
#             game_title=game_title,
#             platform=platform
#         )
#
#         messages.success(request, f'Successfully registered for {registered_event.event_name} ({registered_event.game_title}).')
#         return redirect('profile')  # Redirect to profile or any other page
#
#     return render(request, 'register_event.html')  # Render the registration page

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RegisteredEvents


# def view_registered_events(request):
#     registered_events = RegisteredEvents.objects.filter(user=request.user)
#     return render(request, 'view_registered_events.html', {'registered_events': registered_events})

def search_games(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        games = Game.objects.filter(title__icontains=query) | Game.objects.filter(genre__icontains=query)
        results = [
            {
                "title": game.title,
                "summary": game.summary[:100],  # Return a shortened version of the summary
                "genre": game.genre,
                "image_url": game.image.url if game.image else None,
                "available_devices": game.available_devices,
                "pricing": game.pricing,
            }
            for game in games
        ]

    return JsonResponse({"results": results})


def event_list(request):
    events = Event.objects.all()
    user_registrations = Registration.objects.filter(user=request.user)
    registered_events = [reg.event.id for reg in user_registrations]
    return render(request, 'join.html', {'events': events, 'registered_events': registered_events})


def game_details(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    required_specs = RequiredSpecs.objects.get(game=game)

    # Fetching the current specs for the logged-in user
    try:
        current_specs = CurrentSpecs.objects.get(user=request.user)
    except CurrentSpecs.DoesNotExist:
        current_specs = None  # Handle if no specs exist for the user

    context = {
        "game": game,
        "required_specs": required_specs,
        "current_specs": current_specs
    }
    return render(request, 'game_details.html', context)
