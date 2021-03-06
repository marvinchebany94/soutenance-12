"""epicevents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db import router
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,\
    TokenRefreshView,\
    TokenVerifyView

from app.views import connexion_view, ClientsView, ContratsView, EventsView

router = routers.SimpleRouter()
router.register('clients', ClientsView, basename='clients')
router.register('contrats', ContratsView, basename='contrat')
router.register('events', EventsView, basename='events')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name="gettoken"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="refreshtoken"),
    path('verifytoken/', TokenVerifyView.as_view(), name="verifytoken"),
    path('login/', connexion_view, name="login"),
    path('api/clients/<pk>/', ClientsView.as_view({
            'patch': 'partial_update'
        })),
    path('api/clients/', ClientsView.as_view({
        "post": "create",
        "get": "get_queryset"
    })),
    path('api/contrats/<pk>/', ContratsView.as_view({
            'patch': 'partial_update',
            'get': 'get_queryset'
        })),
    path('api/contrats/', ContratsView.as_view({
            'get': 'get_queryset',
            'post': 'create',
        })),
    path('api/clients/<pk>/events/', EventsView.as_view({
        'post': 'create'
    })),
    path('api/events/', EventsView.as_view({
        'get': 'get_queryset'
    })),
    path('api/events/<pk>/', EventsView.as_view({
        'patch': 'partial_update',
    })),
]

"""

"""