from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("sentry-debug/", trigger_error),
    path("admin/", admin.site.urls),
    path("health/", lambda _:JsonResponse({"detail":"Healthy"}),name="health"),
    path("api/",include(
        [
            #Token Generate
            #---------------------------------------------------------------------
            path('token/access/',TokenObtainPairView.as_view(),name='access-token'),
            path('token/refresh/',TokenRefreshView.as_view(),name='refresh-token'),
            path('token/verify/',TokenVerifyView.as_view(),name='verify-token'),

            #Project apps urls
            #---------------------------------------------------------------------
            path('users/',include('user.urls')),
            path('chats/',include('chat.urls')),
            path('groups/',include('group.urls')),
            path('channels/',include('channel.urls')),
            path('',include('share.urls')),

            #Swagger path
            #---------------------------------------------------------------------
            path('schema/', SpectacularAPIView.as_view(), name='schema'),
            path('swagger/', SpectacularSwaggerView.as_view(), name='swagger'),
            path('redoc/', SpectacularRedocView.as_view(), name='redoc'),

        ]
    ))
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=debug_toolbar_urls()