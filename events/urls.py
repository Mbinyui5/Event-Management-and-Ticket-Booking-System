from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list_view, name='event_list'),
    path('event/<int:pk>/', views.event_detail_view, name='event_detail'),
    path('event/new/', views.event_create_view, name='event_create'),
    path('event/<int:pk>/edit/', views.event_update_view, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete_view, name='event_delete'),
    
    # API endpoints
    path('api/events/', views.api_event_list, name='api_event_list'),
]
