import jwt
from datetime import datetime, timedelta
import jwt
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from otp_project.settings import SECRET_KEY
from .models import Student

def generate_jwt_token(student, device_id):
    payload = {
        'enrollment_no': student.enrollment_no,
        'device_id': device_id,  # include device ID in token
        'exp': datetime.utcnow() + timedelta(days=90),  # token expiration
    }
    token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')
    return token

def verify_jwt_token(token):
    try:
        # Decode the token to retrieve the payload
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Get the enrollment_no and device_id from the decoded token
        enrollment_no = decoded_token['enrollment_no']
        device_id = decoded_token['device_id']

        # Check if the student with the enrollment_no exists
        try:
            student = Student.objects.get(enrollment_no=enrollment_no)
        except Student.DoesNotExist:
            return None  # If the student doesn't exist, return None

        # Optionally, you can also check if the device_id matches (for extra security)
        if not student.device.device_id == device_id:
            return None  # If the device doesn't match, return None
        
        # If everything is valid, return the student object
        return student

    except ExpiredSignatureError:
        # Token is expired
        return None
    except InvalidTokenError:
        # Token is invalid (e.g., tampered or incorrectly formatted)
        return None