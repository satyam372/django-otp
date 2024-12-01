from asyncio.log import logger
from MySQLdb import IntegrityError
from otp_app.security.token import generate_jwt_token, verify_jwt_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from otp_app.security.decryption import decrypt_data
from otp_app.security.keys import GeneratePublicPrivateKey
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
from .models import Student, Device
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization

from django.views import View
from django.http import JsonResponse
from django.urls import resolve
import json
from django.utils.deprecation import MiddlewareMixin

import logging

logger = logging.getLogger(__name__)


def load_private_key_from_file(file_path):
    with open(file_path, 'rb') as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

def decrypt_key(encrypted_key_base64, private_key):
    # Decode the base64 encoded encrypted key
    encrypted_key = base64.b64decode(encrypted_key_base64)
    # Decrypt the key using the RSA private key
    decrypted_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )
    return decrypted_key



class CheckRegistrationStatus(APIView):

    def post(self, request):
        encrypted_enrollment_no_base64 = request.data.get('enrollment_no')
        device_id_base64 = request.data.get('device_id')
        key_base64 = request.data.get('key')
        iv = request.data.get('iv')
        
        private_key_path = "C://Users//Satyam//Desktop//otp_project//private_key.pem"
        try:
            private_key = load_private_key_from_file(private_key_path)
            decrypted_key = decrypt_key(key_base64, private_key)
            enrollment_no = decrypt_data(encrypted_enrollment_no_base64, decrypted_key, iv)
            device_id = decrypt_data(device_id_base64, decrypted_key, iv)

            if enrollment_no:
                try:
                    student = Student.objects.get(enrollment_no=enrollment_no)
                except Student.DoesNotExist:
                    return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
                
                student_name = student.name
                student_department = student.department
                student_specialization = student.specialization  

            try:
                Device.objects.get(enrollment_no=student, device_id=device_id)
                token = generate_jwt_token(student, device_id)
                return Response({
                    "message": "Existing user re-authenticated, new token issued.",
                    "token": token,
                    "name": student_name,
                    'department': student_department,
                    'specialization': student_specialization
                }, status=status.HTTP_200_OK)
            
            except Device.DoesNotExist:
                # Register new device
                try:
                    Device.objects.create(enrollment_no=student, device_id=device_id)
                    token = generate_jwt_token(student, device_id)
                    return Response({
                        "message": "New user registered successfully",
                        "token": token,
                        "name": student_name
                    }, status=status.HTTP_201_CREATED)
                
                except IntegrityError:
                    return Response(
                        {"error": "This student is already registered with another device."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        except Exception as e:
            # General error for other decryption failures
            logger.error("Decryption error: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Verify_Token(APIView):

    def post(self, request):
        token = request.data.get('token')
        if token:
            student = verify_jwt_token(token)  
            if student: 
                return Response({"message": "Authenticated successfully"}, status=status.HTTP_200_OK)
            else:  
                return Response({"message": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

class GetPublicKey(APIView):
    def post(self, request):  
        try:
            key_generator = GeneratePublicPrivateKey()
            key_generator.generate_keys()
            public_key = key_generator.get_public_key()
            private_key = key_generator.get_private_key()
            key_generator.save_private_key_to_file("/etc/django_keys/private_key.pem")
            key_generator.save_public_key_to_file("/etc/django_keys/public_key.pem")

            return Response({"public_key": public_key.decode('utf-8')}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Error generating public key: %s", e)
            return Response(
                {"error": "Failed to generate public key"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
