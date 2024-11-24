from django.template.response import TemplateResponse
from django.http import JsonResponse
from otp_app.views import CheckRegistrationStatus, Verify_Token, GetPublicKey
import json
import logging

logger = logging.getLogger(__name__)
# class ApiProxyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.path == '/proxy/':
#             if request.method == 'POST':
#                 try:
#                     data = json.loads(request.body)
#                     target = data.get('target')

#                     route_map = {
#                         "register": CheckRegistrationStatus,
#                         "verify_token": Verify_Token,
#                         "get_key": GetPublicKey
#                     }

#                     if target in route_map:
#                         view_class = route_map[target]
#                         view_instance = view_class.as_view()
#                         response = view_instance(request)
#                         if hasattr(response, 'render'):
#                             response.render()
#                         return response

#                     return JsonResponse({"error": "Invalid target specified"}, status=400)

#                 except json.JSONDecodeError:
#                     return JsonResponse({"error": "Malformed request body"}, status=400)
#                 except Exception as e:
#                     return JsonResponse({"error": str(e)}, status=500)

#         response = self.get_response(request)
#         return response


class ApiProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/proxy/':
            if request.method == 'POST':
                try:
                    data = json.loads(request.body)
                    target = data.get('target')
                    payload = data.get('payload', {})

                    # Create a new request.data with the payload
                    request._body = json.dumps(payload).encode('utf-8')

                    route_map = {
                        "register": CheckRegistrationStatus,
                        "verify_token": Verify_Token,
                        "get_key": GetPublicKey
                    }

                    if target in route_map:
                        view_class = route_map[target]
                        view_instance = view_class.as_view()
                        response = view_instance(request)
                        if hasattr(response, 'render'):
                            response.render()
                        return response

                    return JsonResponse({"error": "Invalid target specified"}, status=400)

                except json.JSONDecodeError:
                    return JsonResponse({"error": "Malformed request body"}, status=400)
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=500)

        response = self.get_response(request)
        return response