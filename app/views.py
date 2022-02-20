from datetime import datetime

import pytz
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
# Create your views here.
from app.serializers import UserSerializers, ClientsSerializers, \
    ContratsSerializers
from .models import User, Clients, Contrats
from .permissions import EquipeDeVente
from .my_own_fonctions import verifiy_pk


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


class ClientsView(ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self):
        if self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            try:
                int(pk)
            except ValueError:
                return Response('Tu dois entrer un chiffre.',
                                status=status.HTTP_404_NOT_FOUND)
            try:
                Clients.objects.get(id=int(pk))
                print(Clients.objects.get(id=pk).email)
            except ObjectDoesNotExist:
                return Response("Le client n'existe pas.",
                                status=status.HTTP_404_NOT_FOUND)
            print('probleme ici')
            return self.queryset.filter(id=pk).values()

        else:
            return Response("Tu dois entrer un chiffre afin de trouver \
le client", status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        if request.user.equipe == 'gestion':
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
gestion.", status=status.HTTP_403_FORBIDDEN)
        serializers = ClientsSerializers(data=request.data)
        if serializers.is_valid():
            sales_contact = serializers.data['sales_contact']
            try:
                User.objects.get(email=sales_contact, equipe="vente")
            except ObjectDoesNotExist:
                return Response("L'email ne correspond pas à l'email d'un \
membre de l'équipe de vente.",
                                status=status.HTTP_404_NOT_FOUND)
            try:
                serializers.save()
                return Response("formulaire enregistré")
            except IntegrityError:
                return Response("Formulaire non enregistré dans la base de \
données.", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializers.errors)

    def partial_update(self, request, *args, **kwargs):
        if request.user.equipe == 'gestion':
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
        gestion.", status=status.HTTP_403_FORBIDDEN)
        if not self.kwargs.get('pk'):
            return Response("Tu dois entrer un chiffre.",
                            status=status.HTTP_404_NOT_FOUND)
        else:
            pk = self.kwargs.get('pk')
            try:
                int(pk)
            except ValueError:
                return Response("Tu dois entrer un chiffre.",
                                status=status.HTTP_404_NOT_FOUND)
            client = get_object_or_404(Clients, id=pk,
                                       sales_contact=request.user)
            serializers = ClientsSerializers(client, data=request.data,
                                             partial=True)
            if serializers.is_valid():
                try:
                    serializers.save()
                    client.date_updated = timezone.now()
                    client.save()
                    return Response(serializers.data)
                except IntegrityError:
                    return Response("erreur pendant l'enregistrement du \
client.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializers.errors)


class ContratsView(ModelViewSet):
    queryset = Contrats.objects.all()
    serializer_class = ContratsSerializers
    permission_classes = [EquipeDeVente]
    authentication_classes = [JWTAuthentication]
    
    #url api/contrats/<pk_contrat>/
    def get(self):
        """
            Ajoutez une url pour voir tous les contrats d'un client
            api/clients/<pk>/contrats/
        """
        if self.request.user.equipe == 'gestion':

            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
gestion.", status=status.HTTP_403_FORBIDDEN)
        else:
            if not self.kwargs.get('pk_contrat'):
                try:
                    contrats = self.queryset.filter(
                        sales_contact=self.request.user)
                    return contrats
                except ObjectDoesNotExist:
                    return Response("Tu n'as aucun contrat pour le moment",
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                pk = self.kwargs.get('pk_contrat')
                try:
                    int(pk)
                except ValueError:
                    return Response("Tu dois entrer un chiffre.",
                                    status=status.HTTP_404_NOT_FOUND)
                contrat = get_object_or_404(Contrats, id=pk,
                                            sales_contact=self.request.user)
                return contrat

    def create(self, request, *args, **kwargs):
        """
            à voir si un client peut avoir un ou plusieurs contrat
        """
        if not request.user.has_sales_permissions():
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
gestion.", status=status.HTTP_403_FORBIDDEN)
        else:
            form = self.serializer_class(data=request.data)
            if form.is_valid():
                form.validated_data['sales_contact'] = request.user
                form.save()
                return Response(form.data)
            else:
                return Response(form.errors)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.has_sales_permissions():
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
gestion.", status=status.HTTP_403_FORBIDDEN)
        else:
            if not verifiy_pk(self.kwargs.get('pk')):
                return Response("Tu dois entrer l'id du contrat.",
                                status=status.HTTP_404_NOT_FOUND)
            else:
                pk = verifiy_pk(self.kwargs.get('pk'))
                contrat = get_object_or_404(Contrats,
                                            id=pk,
                                            sales_contact=request.user)
                serializer = ContratsSerializers(contrat,
                                                 data=request.data,
                                                 partial=True)
                if serializer.is_valid():
                    try:
                        serializer.save()
                        contrat.date_updated = timezone.now()
                        contrat.save()
                        return Response(serializer.data)
                    except IntegrityError:
                        return Response("Erreur pendant la modification.",
                                        status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(serializer.errors)

        """
        if not self.kwargs.get('pk_contrats'):
            return Response("Tu dois entrer un chiffre.",
                            status=status.HTTP_404_NOT_FOUND)
        else:
            pk = self.kwargs.get('pk')
            try:
                int(pk)
            except ValueError:
                return Response("Tu dois entrer un chiffre.",
                                status=status.HTTP_404_NOT_FOUND)
            client = get_object_or_404(Clients, id=pk,
                                       sales_contact=request.user)
            serializers = ClientsSerializers(client, data=request.data,
                                             partial=True)
            if serializers.is_valid():
                try:
                    serializers.save()
                    return Response(serializers.data)
                except IntegrityError:
                    return Response("erreur pendant l'enregistrement du \
        client.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializers.errors)

"""












