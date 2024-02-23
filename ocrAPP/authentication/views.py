from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser
import json

# Create your views here.
def home(request):
    return render(request,'index.html')

def login(request):
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
        if CustomUser.objects.filter(phone_number=data['phone_number']).exists():
            return JsonResponse({'message':'A user with this phone number already exists.'}, status=400)
        try:
            user = CustomUser(
                username = data['username'],
                password = make_password(data['password']),
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