from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    # path("sentry-debug/", trigger_error),
    path("admin/", admin.site.urls),
    path("api/",include(
        [
            #Token Generate
            path('token/access/',TokenObtainPairView.as_view(),name='access-token'),
            path('token/refresh/',TokenRefreshView.as_view(),name='refresh-token'),
            path('token/verify/',TokenObtainPairView.as_view(),name='verify-token'),


            #Swagger path
            path('schema/', SpectacularAPIView.as_view(), name='schema'),
            path('swagger/', SpectacularSwaggerView.as_view(), name='swagger'),
            path('redoc/', SpectacularRedocView.as_view(), name='redoc'),

        ]
    ))
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)