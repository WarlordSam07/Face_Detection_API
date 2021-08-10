from flask import Flask, render_template, Response, request
import cv2
app=Flask(__name__)
camera = cv2.VideoCapture(0)


def gen_frames():  
    while True:
        success, f2 = camera.read()  # read the camera frame
        if not success:
            break
        else:
            detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            faces=detector.detectMultiScale(f2,1.1,7)
             #Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(f2, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText("Face Detecting...",(210,190), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
            key = cv2.waitKey(1)
            if key==81 or key==113:
                break
            camera.release()
            ret, buffer = cv2.imencode('.jpg', f2)
            f2 = buffer.tobytes()
            
            yield (b'--f2\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + f2 + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed',methods = ['POST','GET'])
def res():
	global result
	if request.method == 'POST':
		result = request.form.to_dict()
		return render_template("result.html",result = result)
@app.route('/results')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=f2')
if __name__=='__main__':
    app.run(debug=True)