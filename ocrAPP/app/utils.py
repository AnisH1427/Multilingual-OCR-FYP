# utils.py
import cv2
import numpy as np
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder
from mltu.transformers import ImageResizer

class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, model_path: str, vocab: list, *args, **kwargs):
        super().__init__(model_path=model_path, *args, **kwargs)
        self.vocab = vocab

    def predict(self, image: np.ndarray):
        
        image = cv2.resize(image, (1408, 96))
        
        # Ensure the image has 3 color channels
        if image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
        # kernel = np.ones((5,200), np.uint8)
        # img_dilation = cv2.dilate(thresh, kernel, iterations=1)

         # Find contours
        # contours, hierarchy = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours based on their bounding box coordinates
        # bounding_boxes = [cv2.boundingRect(ctr) for ctr in contours]
        # sorted_contours = [ctr for _, ctr in sorted(zip(bounding_boxes, contours), key=lambda pair: pair[0][1])]
        
         # Create a list to store predicted texts
        # predicted_texts = []
        
        # # Add an extra dimension for the batch size
        image_pred = np.expand_dims(image, axis=0).astype(np.float32)
        
        # #loop over sorted contours
        # for i, ctr in enumerate(sorted_contours):
        #     # Get bounding box
        #     x, y, w, h = cv2.boundingRect(ctr)

        #     # Getting ROI
        #     roi = image[y:y+h, x:x+w]
        #     roi_row = roi.shape[0]
        #     roi_col = roi.shape[1]

        #     # Show ROI
        #     if(roi_row>3000 or roi_row<=20 or roi_row<=10 or roi_col<=110):
        #         continue
            

        preds = self.model.run(None, {self.input_name: image_pred})[0]
        text = ctc_decoder(preds, self.vocab)[0]
        return text
    
def detect_contours(image,language="English"):
    color_image = image.copy()
    
    # Check the number of channels in the image
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    else:
        color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # The image is already grayscale
        gray = image

    # Convert grayscale image to binary
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    # cv2_imshow(thresh)

    # Dilation
    kernel = np.ones((5, 200), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours
    contours, hierarchy = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours based on their bounding box coordinates
    bounding_boxes = [cv2.boundingRect(ctr) for ctr in contours]
    sorted_contours = [ctr for _, ctr in sorted(zip(bounding_boxes, contours), key=lambda pair: pair[0][1])]

    # Loop over sorted contours
    k = 0
    for i, ctr in enumerate(sorted_contours):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = color_image[y:y+h, x:x+w]
        roi_row, roi_col, _ = roi.shape  # Get ROI dimensions

        # Show ROI
        if roi_row > 3000 or roi_row <= 20 or roi_row <= 10 or roi_col <= 110:
            continue

        # if h > 60:
        #     # Split ROI into two separate ROIs vertically
        #     roi1 = roi[:h//2, :]
        #     roi2 = roi[h//2:, :]

        #     # Update rectangle for the first ROI
        #     cv2.rectangle(color_image, (x, y), (x + w, y + h//2), (90, 180, 255), 2)

        #     # Update rectangle for the second ROI
        #     cv2.rectangle(color_image, (x, y + h//2), (x + w, y + h), (90, 180, 255), 2)

        #     k += 2
        
        # Update rectangle for the ROI
        cv2.rectangle(color_image, (x, y), (x + w, y + h), (90, 0, 255), 2)

        k += 1

    # Scale the image to fit a specific size
    # Replace MAX_WIDTH and MAX_HEIGHT with the desired dimensions
    MAX_WIDTH = 800
    MAX_HEIGHT = 600

    height, width = color_image.shape[:2]
    scale = min(MAX_WIDTH / width, MAX_HEIGHT / height)
    resized_image = cv2.resize(color_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    return resized_image