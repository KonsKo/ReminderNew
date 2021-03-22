from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('create/', views.CreateRemView.as_view(), name='create_rem'),
    path('update/<int:pk>', views.UpdateRemView.as_view(), name='update_rem'),
    path('read/<int:pk>', views.ReadRemView.as_view(), name='read_rem'),

    path('ajax-change-status', views.change_status, name='ajax_change_status'),
]