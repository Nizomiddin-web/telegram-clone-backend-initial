from django.urls import path

from share.views import SearchView

urlpatterns = [
    path('search/<str:query>/',SearchView.as_view(),name='search-view')
]