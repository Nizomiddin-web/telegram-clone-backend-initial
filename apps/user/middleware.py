from user.models import DeviceInfo
from django.utils import timezone


class TrackLoginActivityMiddleware:
    """
    Middleware to track the login IP address and device information of users.
    """
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            ip_address = self.get_client_ip(request)
            user_agent = request.headers.get("user-agent","unknown device")
            request.user.is_online = True
            request.user.last_seen = timezone.now()
            request.user.last_login = timezone.now()
            request.user.save(update_fields=["is_online","last_seen","last_login"])

            if not DeviceInfo.objects.filter(
                user=request.user,ip_address=ip_address
            ).exists():
                DeviceInfo.objects.create(
                    user=request.user,
                    device_name=user_agent,
                    ip_address=ip_address,
                    last_login=timezone.now()
                )
        return response

    def get_client_ip(self,request):
        """
        Get the client ip address from request
        """
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

