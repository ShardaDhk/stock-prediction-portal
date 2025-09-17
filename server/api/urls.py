from django.urls import path
from accounts import views as UserViews

urlpatterns = [
    path('register/', UserViews.ResgisterView.as_view()), #as_views because it is class based view
    
]