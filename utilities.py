import tensorflow as tf
import cv2
import numpy as np
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
from rest_framework.response import Response

def analysis(path):
    filename = settings.BASE_DIR/'analysis/machine_learning_model/machine_learning.h5'
    model = tf.keras.models.load_model(filename)
    img = cv2.imread(path)
    if img is None: return 'Error: Could not read image file'
    # Preprocess the image
    SIZE = 224
    img = cv2.resize(img, (SIZE, SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = img / 255
    img = np.expand_dims(img, axis=0) # Add batch dimension

    # Pass the preprocessed image through the model
    predictions = model.predict(img)
    # Get the predicted class label
    prediction = np.argmax(model.predict(img)) 
    # Define the label names
    labels = ['comedonal acne valgum', 'cystic acne', 'freckles', 'inflammatory acne', 'melasma']
    # Create a LabelEncoder object and fit it to the label names
    le = LabelEncoder()
    le.fit(labels)
    # Get the predicted class label
    prediction = np.argmax(model.predict(img)) 
    decoded_prediction = le.inverse_transform([prediction])
    
    return decoded_prediction
