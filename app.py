import os
import uuid
import urllib
from PIL import Image
import streamlit as st
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR, 'CIFAR10_best.h5'))

ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXT


def predict(filename, model):
    img = load_img(filename, target_size=(32, 32))
    img = img_to_array(img)
    img = img.reshape(1, 32, 32, 3)

    img = img.astype('float32')
    img = img / 255.0
    result = model.predict(img)

    dict_result = {result[0][i]: classes[i] for i in range(10)}

    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]

    prob_result = [(prob[i] * 100).round(2) for i in range(3)]
    class_result = [dict_result[prob[i]] for i in range(3)]

    return class_result, prob_result


def main():
    st.title("Image Classifier")

    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png', 'jfif'])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

            class_result, prob_result = predict(uploaded_file, model)

            predictions = {
                "class1": class_result[0],
                "class2": class_result[1],
                "class3": class_result[2],
                "prob1": prob_result[0],
                "prob2": prob_result[1],
                "prob3": prob_result[2],
            }

            st.write(predictions)

        except Exception as e:
            st.error("Error processing image: " + str(e))

if __name__ == "__main__":
    main()
