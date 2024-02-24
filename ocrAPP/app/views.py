# views.py
from django.shortcuts import render
from .utils import ImageToWordModel
import cv2
import numpy as np

def home(request):
    if request.method == 'POST' and 'document' in request.FILES:
        uploaded_file = request.FILES['document']
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        # Model path and vocabulary list
        model_path = "Model/202402171624/model.onnx"
        vocab = ['i', '3', 'O', 'C', 'P', '1', 'p', ',', 'H', '?', '6', 'x', '-', '8', 'g', 'T', 't', '!', 'c', 'G', 'U', 'D', 'V', 'R', 'a', 'u', '#', 'Y', 'Q', '.', ':', '9', 'K', 'b', 'I', 'r', '(', 'j', '&', 'f', 'n', 'Z', 'd', '5', 'L', 'J', '4', 'B', 'v', 'w', ')', "'", 'N', 'm', 'M', 'h', 'k', '*', '7', 'F', 'S', '+', '2', 'q', '"', '0', 'X', 'z', ' ', 'o', 'W', 'e', ';', 'y', 'E', 'A', 's', '/', 'l']

        # Create the model
        model = ImageToWordModel(model_path=model_path, vocab=vocab)

        # Predict the text
        prediction_text = model.predict(image)

        return render(request, 'home.html', {'prediction_text': prediction_text})

    return render(request, 'home.html')