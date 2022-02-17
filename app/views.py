from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
# Create your views here.
from app.serializers import UserSerializers
from .models import User


@api_view(['POST'])
def connexion_view(request):
    if request.POST.get('email') and request.POST.get('password'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response("Aucun compte n'existe avec cet email.",
                            status=status.HTTP_404_NOT_FOUND)
        if user.check_password(password):
            request.user = authenticate(request, email=email, password=password)
            if request.user.is_authenticated:

                return Response('Tu es connecté.')
            else:
                return Response(request.user.is_authenticated)
        else:
            if not request.user.is_authenticated:
                return Response("Mot de passe invalide.",
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Tu dois entrer ton email et mdp.",
                        status=status.HTTP_404_NOT_FOUND)







