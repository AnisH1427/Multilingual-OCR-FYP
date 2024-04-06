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
from rest_framework.views import APIView
from rest_framework.response import Response
from mltu.configs import BaseModelConfigs
from .utils import ImageToWordModel

class PredictView(APIView):
    def post(self,request,format=None):
        if 'document' not in request.FILES:
            return Response({'error': 'No document file provided'}, status=400)
        uploaded_file = request.FILES['document']
        
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        configs = BaseModelConfigs.load("Model/202403031722/configs.yaml")

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
            
@login_required(login_url='login_with_token/')
def home(request):
    
        

    return render(request, 'home.html')
