import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import time
import numpy as np
from playsound import playsound
from flask import Flask, render_template, request

from cloudant.client import Cloudant

client = Cloudant.iam(account_name="eb433409-a69f-477a-9c62-b277c3cd23dc-bluemix",api_key="i7viH79onAkYy7kVE9A6ArJtvaXsHLB0brw_ovxJbw1i",connect = True)

db = client.create_database('my_database')

app = Flask(__name__)

# home page
@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

# registration page
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/afterreg',methods=['POST','GET'])
def afterreg():
    name = request.form['name']
    email = request.form['email']
    password = request.form['pwd']

    x = [x for x in request.form.values(name,email,password)]
    print(x)
    data = {
        'email': x[1],
        'name': x[0],
        'pwd': x[2]
    }
    print(data)

    query = {'email': {'$eq': data['email']}}

    docs = db.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if (len(docs.all())==0):
        url = db.create_document(data)

        # response = request.get(url)
        return render_template('register.html', pred = "Registration  Successful!, please login using your details")
    else:
        return render_template('register.html', pred = "Already registered!, please login using your details")

# login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/afterlogin', methods=['POST'])
def afterlogin():
    username = request.form.get('email')
    password = request.form.get('pwd')
    print(username,password)

    query = {'email': {'$eq': username}}

    docs = db.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if(len(docs.all())==0):
        return render_template('login.html', pred = "The username is not found!")
    else:
        if(username == docs[0][0]['email'] and password == docs[0][0]['pwd']):
            return render_template('prediction.html')
        else:
            print('Invalid User')

# logout page
@app.route('/logout')
def logout():
    return render_template('index.html')

# detection
@app.route('/result', methods=['POST','GET'])
def res():
    webcam =cv2.VideoCapture('drowning.mp4')

    if not webcam.isOpened():
        print("Could not open webcam")
        exit()

    t0 = time.time()

    centre0 = np.zeros(2)
    isDrowning = False

    # loop through frames
    while webcam.isOpened():
        # read frame from webcam
        status, frame = webcam.read()

        bbox, label, conf = cv.detect_common_objects(frame)

        if (len(bbox)>0):
            bbox0 =bbox[0]

            centre = [0,0]

            centre = [(bbox[0]+bbox0[2])/2, (bbox[1]+bbox0[3])/2]

            # vertical and horizontal movement variables
            hmov = abs(centre[0]-centre0[0])
            vmov = abs(centre[1]-centre0[1])

            x= time.time()

            threshold = 10
            if(hmov>threshold or vmov>threshold):
                print(x-t0, 's')
                t0 = time.time()
                isDrowning = False
            else:
                print(x-t0, 's')
                if((time.time() - t0) > 10):
                    isDrowning = True

            print('bbox:', bbox, 'centre:', centre, 'centre0:', centre0)
            print('Is he drowning:', isDrowning)

            centre0 = centre

        out = draw_bbox(frame, bbox, label, conf, isDrowning)

        cv2.imshow("Real-time object detection", out)
        if(isDrowning == True):
            playsound('alarm.mp3')
            webcam.release()
            cv2.destroyAllWindows()
            return render_template('prediction.html', prediction = "Emergency !!! The person is drowning")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()

""" Running the application """
if __name__ == "__main__":
    app.run(debug=True)