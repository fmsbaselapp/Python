
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import exceptions

cred = credentials.Certificate('ServiceAccountTest.json')
firebase_admin.initialize_app(cred)
db = firestore.client()




def testFunc():
   
        num = 1
        message = 'Test'
        db.collection('Nachrichten').document('Schulen').collection(
            'Dreirosen').document('Montag').update({
                'test': message

            })
   

try:
    testFunc()
except exceptions.FirebaseError as ex:
    if ex.code == exceptions.INVALID_ARGUMENT:
        print(ex) # One or more arguments were invalid
    elif ex.code == exceptions.UNAVAILABLE:
        print(ex) # FCM service is temporarily down
    else:
        print(ex) # All other errors



#num: {
#                    u'target': 'klasseTest',
#                    u'klasse': '2B',
#                    u'grund': 'Test GRUND',
#                    u'raum': 'ausgedacht',
#                },