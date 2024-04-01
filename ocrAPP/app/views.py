# views.py
from django.shortcuts import render
from .utils import ImageToWordModel
from .utils import detect_english_contours
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
            image = detect_english_contours(image)
            
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
            
@login_required(login_url='login_with_token/')
def home(request):
    # if request.method == 'POST' and 'document' in request.FILES:
    #     uploaded_file = request.FILES['document']
    #     image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    #     # Check if the image is valid
    #     if image is None:
    #         return HttpResponse('Invalid image', status=400)
    #     image_with_roi = detect_english_contours(image)

        # Check the number of channels in the image
        # if len(image.shape) < 3 or image.shape[2] < 3:
        #     return HttpResponse('Expected a color image', status=400)
        
        # # Model path and vocabulary list
        # model_path = "Model/202403031722/model.onnx"
        # vocab = [')', 'D', 'E', 't', '(', 'U', '8', 'r', 'X', 'P', 'i', 'e', '"', '/', '-', ' ', '5', ':', '&', 'R', '.', 'u', '0', 'h', 'Q', 'H', 'N', 'L', 'S', '#', 'd', 'z', 'M', 'W', 'b', 'K', 'T', 'v', 'Y', 'j', 'w', 'n', 'F', 'J', '4', '!', '*', 'y', 'o', ',', '?', 'C', '7', '3', 'g', 'V', 'm', 's', 'c', 'a', '6', 'G', 'q', 'f', 'p', 'O', "'", '2', 'Z', 'k', 'B', '1', '+', 'l', 'x', ';', '9', 'A', 'I']

        # Create the model
        # model = ImageToWordModel(model_path=model_path, vocab=vocab)

        # Predict the text
        # prediction_text = model.predict(image)

        # return render(request, 'home.html', {'prediction_text': prediction_text})
        

    return render(request, 'home.html')
