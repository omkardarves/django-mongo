from django.urls import path
from .views import MyApiView

urlpatterns = [
    # URL for retrieving all documents
    # path('my-api/', MyApiView.as_view(), name='my_api_list'),
    
    # URL for retrieving a single document by ID
    path('my-api/<str:id>/', MyApiView.as_view(), name='my_api_detail'),
]