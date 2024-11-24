# """
# URL configuration for otp_project project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path
# from otp_app.middleware import ApiProxyMiddleware
# from otp_app.views import CheckRegistrationStatus, Verify_Token
# from otp_app.views import GetPublicKey
# from django.urls import path
# from django.views.decorators.csrf import csrf_exempt

# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     path('register/', CheckRegistrationStatus.as_view(), name = 'register'),
# #     path('verify-token/', Verify_Token.as_view(), name = 'verify-token'),
# #     path('get-key/',GetPublicKey.as_view(), name = 'get-key')
# # ]


# from django.urls import path
# from django.views.decorators.csrf import csrf_exempt

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('proxy/', csrf_exempt(ApiProxyMiddleware().process_request), name='proxy'),
# ]

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from otp_app.middleware import ApiProxyMiddleware

urlpatterns = [
    path('proxy/', csrf_exempt(ApiProxyMiddleware), name='proxy'),
]
