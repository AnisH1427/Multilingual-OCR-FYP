# views.py
from django.shortcuts import render
from .utils import ImageToWordModel
from .utils import detect_contours
import cv2
import numpy as np
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from PIL import Image
import io
import base64
from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer
from rest_framework import status
from django.http import JsonResponse

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
    def create(self, request, *args, **kwargs):
        if 'document' in request.FILES:
            uploaded_file = request.FILES['document']
            image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            
            # Check if the image is valid
            if image is None:
                return Response({'detail': 'Invalid image'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Use the detect_english_contours function to detect contours and draw rectangles on the image
            image = detect_contours(image)
            
            # Convert the image to PIL format
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            # Save the image in a BytesIO object
            byte_arr = io.BytesIO()
            pil_image.save(byte_arr, format=uploaded_file.content_type.split('/')[-1].upper())
            byte_arr.seek(0)
            
            # Return the image
            return HttpResponse(byte_arr, content_type=uploaded_file.content_type)
        
        # Call the super class's create method
        # return super().create(request, *args, **kwargs)
from rest_framework.views import APIView
from rest_framework.response import Response
from mltu.configs import BaseModelConfigs
from .utils import ImageToWordModel

class PredictView(APIView):
    def post(self,request,format=None):
        if 'document' not in request.FILES:
            return Response({'error': 'No document file provided'}, status=400)
        uploaded_file = request.FILES['document']
        
         # Get the language from the request data
        language = request.data.get('language')
        
        if not language:
            return Response({'error': 'No language provided'}, status=400)
        
        # Select the model based on the language
        if language == 'English':
            configs = BaseModelConfigs.load("Model/202404021423/configs.yaml")
        elif language == 'Hindi' or language == 'Nepali':
            configs = BaseModelConfigs.load("Model/Devanagari/202404190616/configs.yaml")
        else:
            return Response({'error': 'Invalid language'}, status=400)
        
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        # configs = BaseModelConfigs.load("Model/202403031722/configs.yaml")

        model = ImageToWordModel(model_path=configs.model_path, vocab=configs.vocab)
        
        #image Preprocessing
        
        # Check the number of channels in the image
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Convert image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
        kernel = np.ones((5,200), np.uint8)
        img_dilation = cv2.dilate(thresh, kernel, iterations=1)
        
        # Find contours
        contours, hierarchy = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours based on their bounding box coordinates
        bounding_boxes = [cv2.boundingRect(ctr) for ctr in contours]
        sorted_contours = [ctr for _, ctr in sorted(zip(bounding_boxes, contours), key=lambda pair: pair[0][1])]

        # Create a list to store predicted texts
        predicted_texts = []
        # Loop over sorted contours
        for i, ctr in enumerate(sorted_contours):
            # Get bounding box
            x, y, w, h = cv2.boundingRect(ctr)

            # Getting ROI
            roi = image[y:y+h, x:x+w]
            roi_row = roi.shape[0]
            roi_col = roi.shape[1]

            # Show ROI
            if(roi_row>3000 or roi_row<=20 or roi_row<=10 or roi_col<=110):
                continue
            # Predict text from the image
            prediction_text = model.predict(roi)

            # Append the prediction along with the bounding box coordinates to the list
            predicted_texts.append((x, y, prediction_text))

        # Sort the list based on y-coordinate, then x-coordinate
        sorted_predictions = sorted(predicted_texts, key=lambda x: (x[1], x[0]))
        final_predictions = [x[2] for x in sorted_predictions]
        print(final_predictions)
        
        # Return the predictions as a JSON response
        return JsonResponse(final_predictions, safe=False)
            
@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile.html',context)


from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from authentication.models import CustomUser
from rest_framework import serializers

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import requests

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'gender']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
class UserUpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
from rest_framework.generics import DestroyAPIView

class UserDeleteView(DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from tensorboard import program

@user_passes_test(lambda u: u.is_superuser)
def tensorboard(request):
    tb1 = program.TensorBoard()
    tb1.configure(argv=[None, '--logdir', 'Model/202404021423/logs'])
    url1 = tb1.launch()

    tb2 = program.TensorBoard()
    tb2.configure(argv=[None, '--logdir', 'Model/Devanagari/202404190616/logs'])
    url2 = tb2.launch()

    return HttpResponse(f'<h2>English Model</h2><iframe src="{url1}" width="100%" height="600"></iframe><h2>Devanagari Model</h2><iframe src="{url2}" width="100%" height="600"></iframe>')

def guide(request):
    return render(request, 'guide.html')