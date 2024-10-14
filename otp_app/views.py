import random
from django.db import IntegrityError
import jwt
from otp_app.token import generate_jwt_token, verify_jwt_token
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .models import Student, Device

class CheckRegistrationStatus(APIView):
    def post(self, request):
        enrollment_no = request.data.get('enrollment_no')
        device_id = request.data.get('device_id')
        # TODO:Encrypt the enrollment_no and device_id
        token = request.data.get('token')

        # Check if the student is in the database
        try:
            student = Student.objects.get(enrollment_no=enrollment_no)
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # Verify the token if present
        if token:
            try:
                # Verify the token validity
                verify_jwt_token(token)
                # If the token is valid then return success
                return Response({"message": "Authenticated successfully"}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                # If the token has expired then allow the user to re-authenticate
                return Response({"message": "Token expired. Please login again."}, status=status.HTTP_401_UNAUTHORIZED)
            except AuthenticationFailed:
                return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # If no token is provided, check if the device is registered
        try:
            Device.objects.get(enrollment_no=student, device_id=device_id)
            # If no token is provided, generate a new one for login
            token = generate_jwt_token(student, device_id)
            return Response({
                "message": "Existing user re-authenticated, new token issued.",
                "token": token
            }, status=status.HTTP_200_OK)

        except Device.DoesNotExist:
            # New user registration case
            try:
                Device.objects.create(enrollment_no=student, device_id=device_id)
                token = generate_jwt_token(student, device_id)

                # Optionally, generate and send OTP
                otp = random.randint(1000, 9999)
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    'your-email@example.com',
                    [student.phone_no],  # Replace with actual phone number or email
                    fail_silently=False,
                )

                return Response({
                    "message": "New user registered successfully", 
                    "otp": otp, 
                    "token": token
                }, status=status.HTTP_201_CREATED)
            
            except IntegrityError:
                return Response(
                    {"error": "This student is already registered with another device."},
                    status=status.HTTP_400_BAD_REQUEST
                )
