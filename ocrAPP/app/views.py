# views.py
from django.shortcuts import render
from .utils import ImageToWordModel
import cv2
import numpy as np
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_with_token/')
def home(request):
    if request.method == 'POST' and 'document' in request.FILES:
        uploaded_file = request.FILES['document']
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        # Model path and vocabulary list
        model_path = "Model/202403031722/model.onnx"
        vocab = [')', 'D', 'E', 't', '(', 'U', '8', 'r', 'X', 'P', 'i', 'e', '"', '/', '-', ' ', '5', ':', '&', 'R', '.', 'u', '0', 'h', 'Q', 'H', 'N', 'L', 'S', '#', 'd', 'z', 'M', 'W', 'b', 'K', 'T', 'v', 'Y', 'j', 'w', 'n', 'F', 'J', '4', '!', '*', 'y', 'o', ',', '?', 'C', '7', '3', 'g', 'V', 'm', 's', 'c', 'a', '6', 'G', 'q', 'f', 'p', 'O', "'", '2', 'Z', 'k', 'B', '1', '+', 'l', 'x', ';', '9', 'A', 'I']

        # Create the model
        model = ImageToWordModel(model_path=model_path, vocab=vocab)

        # Predict the text
        prediction_text = model.predict(image)

        return render(request, 'home.html', {'prediction_text': prediction_text})

    return render(request, 'home.html')
