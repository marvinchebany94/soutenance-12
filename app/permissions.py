from django.core.handlers import exception
from rest_framework import permissions


class EquipeDeVente(permissions.BasePermission):
    """
        L'equipe de vente peut :
            post des clients
            get/patch clients attribués
            get/patch contrats attribués à leur clients
            post evenements pour un contrat
    """
    edit_methods = ('PATCH', 'GET', 'POST', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        if request.user.has_perm('support_permissions'):
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm('support_permissions'):
            return False

        if request.user == obj.sales_contact:
            return True


class EquipeDeGestion(permissions.BasePermission):
    """
        get/patch evenements attriués
        get clients des evenements qui leur sont attribués
    """
    edit_methods = ('GET', 'PATCH')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        if request.user.has_perm('sales_permissions'):
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.equipe == "gestion":
            return True

        if request.user == obj.support_contact:
            return True

        if request.method in self.edit_methods:
            return True
