
from flask import Flask, request
import socket
import numpy as np
import io
import cv2
import json
import base64

#custom
from custom.credentials import token, account
from custom.essentials import stringToRGB, get_model
from custom.whatsapp import whatsapp_message

'''Get host IP address'''
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

app = Flask(__name__)

# Simple http endpoint
@app.route('/get_name', methods = ['GET', 'POST'])
def get_name():
  return 'hello'
  # if request.method == 'POST':
  #   name = request.form.get('name')
  #   return 'your name is '+name

# Simple http endpoint
@app.route('/<string>')
def hello(string):
  return string


@app.route('/encode')
def encode():
  img = 'test_images/test.png'
  # image = cv2.imread(img)
  with open(img, 'rb') as f:
    im_b64 = base64.b64encode(f.read())
  # encoded_string = base64.b64encode(image)
  return im_b64


  


@app.route('/disease_detect', methods=["GET", "POST"])
def disease_detect():
  input_string = request.data
  img = json.loads(input_string)

  #taking input from API request
  patient_name = img['patient name']
  doctor_name = img['doctor name']
  patient_number = img['patient number']
  doctor_number = img['doctor number']
  result_img = stringToRGB(img['img'])
  
  model_name = 'Model/best_model.h5'
  model = get_model()
  model.load_weights(model_name)
  classes = {4: ('nv', ' melanocytic nevi'), 6: ('mel', 'melanoma'), 2 :('bkl', 'benign keratosis-like lesions'), 1:('bcc' , ' basal cell carcinoma'), 5: ('vasc', ' pyogenic granulomas and hemorrhage'), 0: ('akiec', 'Actinic keratoses and intraepithelial carcinomae'),  3: ('df', 'dermatofibroma')}
  img = cv2.resize(result_img, (28, 28))
  result = model.predict(img.reshape(1, 28, 28, 3))
  result = result[0]
  max_prob = max(result)
  

  if max_prob>0.80:
    class_ind = list(result).index(max_prob)
    class_name = classes[class_ind]
    # short_name = class_name[0]
    full_name = class_name[1]
  else:
    full_name = 'No Disease' #if confidence is less than 80 percent then "No disease" 
  

  #whatsapp message
  message = '''
  Patient Name: {}
  Doctor Name: {}
  Disease Name : {}

  '''.format(patient_name, doctor_name, full_name)
  #send whatsapp mesage to patient
  whatsapp_message(token, account, patient_number, message)
  # sleep(5)
  whatsapp_message(token, account, doctor_number, message)
  return 'Success'

  


if __name__ == '__main__':
  # app.debug = True
  app.run(host='0.0.0.0', port=5000, debug=True)


