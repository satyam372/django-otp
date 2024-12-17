from django.template.response import TemplateResponse
from django.http import JsonResponse
from otp_app.views import CheckRegistrationStatus, Verify_Token, GetPublicKey, FetchUser, CreatePastEntry
import json
import logging

class ApiProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/proxy/':
            if request.method == 'POST':
                try:
                    data = json.loads(request.body)  # Parse the request body
                    target = data.get('target')     # Get the target action
                    payload = data.get('payload', {})  # Get the payload

                    # Route map for different targets
                    route_map = {
                        "register": CheckRegistrationStatus,
                        "verify_token": Verify_Token,
                        "get_key": GetPublicKey,
                        "get_user_detail": FetchUser,
                        "save_user_detail": CreatePastEntry,
                        "fetch_user_data": FetchUser,  # Add 'fetch_user_data' target mapped to FetchUser view
                    }

                    # Check if the target is valid
                    if target in route_map:
                        view_class = route_map[target]
                        view_instance = view_class.as_view()

                        # Handle specific cases based on the target
                        if target == "save_user_detail":
                            # Ensure payload contains the necessary fields
                            required_fields = ["rollno", "name", "intime", "outtime", "department"]
                            missing_fields = [field for field in required_fields if field not in payload]

                            if missing_fields:
                                return JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

                            # Attach the payload directly to request.data
                            request._body = json.dumps(payload).encode('utf-8')

                        elif target == "fetch_user_data":
                            # Ensure the payload is a string
                            if not isinstance(payload, str):
                                return JsonResponse({"error": "Payload must be a string for fetch_user_data"}, status=400)

                            # Convert string payload to the expected format (e.g., enrollment number)
                            request._body = json.dumps({"enrollment_no": payload}).encode('utf-8')

                        # Process the request via the mapped view
                        response = view_instance(request)

                        # Render response if necessary
                        if hasattr(response, 'render'):
                            response.render()
                        return response

                    # Return error if target is invalid
                    return JsonResponse({"error": "Invalid target specified"}, status=400)

                except json.JSONDecodeError:
                    return JsonResponse({"error": "Malformed request body"}, status=400)
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=500)

        # Call the default get_response method for other requests
        response = self.get_response(request)
        return response
