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
        # Resize the image to the expected dimensions
        image = cv2.resize(image, (1408, 96))

        # Ensure the image has 3 color channels
        if image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        # Add an extra dimension for the batch size
        image_pred = np.expand_dims(image, axis=0).astype(np.float32)

        preds = self.model.run(None, {self.input_name: image_pred})[0]
        text = ctc_decoder(preds, self.vocab)[0]
        return text