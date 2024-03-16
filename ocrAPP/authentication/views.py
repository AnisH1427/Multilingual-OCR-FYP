from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser
import json
from django.contrib.auth import get_user_model
from django.contrib.auth import login 
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
import requests
from django.core.exceptions import ValidationError

# Create your views here.
def home(request):
    return render(request,'index.html')

def loginpage(request):
    return render(request,'login.html')

from django.core.exceptions import ValidationError
from rest_framework import generics
from .serializers import RegisterSerializer

class CustomRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Verify the reCAPTCHA response
        recaptcha_response = data.get('g-recaptcha-response')
        data = {
            'secret': '6LfrX4cpAAAAAGgep1z-00Ig8lWpGicNIm8_uJJV',
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result['success']:
            return JsonResponse({'message': 'Invalid reCAPTCHA. Please try again.'}, status=400)

        if CustomUser.objects.filter(phone_number=data['phone_number']).exists():
            return JsonResponse({'message':'A user with this phone number already exists.'}, status=400)
        try:
            user = CustomUser(
                username = data['username'],
                # password = make_password(data['password']),
                password = data['password'],
                email = data['email'],
                phone_number = data['phone_number'],
                address = data['address'],
                gender = data['gender']
            )
            user.full_clean()
            user.save()
            return JsonResponse({'message':'User created successfully'}, status=201)
        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return render(request,'signup.html')
    
def login_with_token(request):
    token_key = request.GET.get('token')
    if token_key:
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            login(request,user)
            return redirect('/app/home/')
        except Token.DoesNotExist:
            return JsonResponse({'message':'Invalid token'}, status=400)
    else:
        return JsonResponse({'message':'Token parameter is missing'}, status=400)
