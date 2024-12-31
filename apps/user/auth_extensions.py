from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme

from user.authentications import CustomJWTAuthentication


class CustomJWTAuthenticationSchema(SimpleJWTScheme):
    name = "CustomJWTAuth"
    target_class = CustomJWTAuthentication

