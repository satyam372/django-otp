from rest_framework import serializers
from .models import Student, Device


class DeviceSerialization(serializers.ModelSerializer):

    class Meta:
        model  = Device
        fields = ['enrollment_no']