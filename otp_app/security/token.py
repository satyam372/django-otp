import jwt
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from otp_project.settings import SECRET_KEY
from otp_app.models import Student

def generate_jwt_token(student, device_id):
    payload = {
        'enrollment_no': student.enrollment_no,
        'device_id': device_id,  
        'exp': datetime.utcnow() + timedelta(days=90), 
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        enrollment_no = decoded_token.get('enrollment_no')
        device_id = decoded_token.get('device_id')

        if not enrollment_no or not device_id:
            return None 
        try:
            student = Student.objects.get(enrollment_no=enrollment_no)
        except Student.DoesNotExist:
            return None  
        if student.device.device_id != device_id:
            return None  
        
        return student

    except ExpiredSignatureError:
        print("Token expired")
        return None
    except InvalidTokenError:
        print("Invalid token")
        return None
    except Exception as e:
        print(f"Error during token verification: {e}")
        return None

