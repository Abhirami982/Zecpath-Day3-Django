
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class RoleMiddleware:
    """
    Identifies the role of session-authenticated
    and JWT-authenticated users.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.user_role = None

        # Authenticate using JWT if the user is not
        # already authenticated through a session.
        if not request.user.is_authenticated:
            try:
                result = JWTAuthentication().authenticate(request)

                if result is not None:
                    request.user, token = result

            except AuthenticationFailed:
                pass

        # Identify the user's role.
        if request.user.is_authenticated:
            request.user_role = getattr(
                request.user, "role", None
            )

        response = self.get_response(request)

        return response
