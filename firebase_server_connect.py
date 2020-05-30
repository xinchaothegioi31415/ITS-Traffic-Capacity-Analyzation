from firebase import firebase
import pyrebase
import threading
import time

config = {
    "apiKey": "AIzaSyCxyEHca1eSWz8JT9NiLGJTEApG94moaBU",
    "authDomain": "smarttraffic-2a170.firebaseapp.com",
    "databaseURL": "https://smarttraffic-2a170.firebaseio.com",
    "projectId": "smarttraffic-2a170",
    "storageBucket": "smarttraffic-2a170.appspot.com",
    "messagingSenderId": "383660536137",
    "appId": "1:383660536137:web:ad65074671a9dc822c2a98",
    "serviceAccount": "./ServiceAccount.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class FirebaseManager(object):   
    def update_capacity(self, parent_camera, capacity_value):
        db.child(parent_camera).update({"capacity": round(capacity_value * 100, 2)})
        db.update({"time": int(time.time())})

    def update_time(self):
        db.update({"time": int(time.time())})
            
    def update_level(self,parent_camera, parent_name,level):
        db.child(parent_camera).update({parent_name: level})
        
    def update_current_time_video(self, parent_camera, parent_name, position):
        db.child(parent_camera).update({parent_name: position})

