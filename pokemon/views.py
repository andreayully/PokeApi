from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from pokemon.models import *
from pokemon.serializers import PokemonSerializer
from rest_framework import status


class CustomAPIException(ValidationError):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class PokemonListCreateView(generics.ListAPIView):
    """
    List of pokemon stored in django models
    """
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'id_poke_api']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        data = self.request.GET
        if 'name' in data:
            self.queryset = self.queryset.filter(name__icontains=data['name'])
        return self.queryset


class PokemonRetrieveView(generics.RetrieveAPIView):
    """
    Retrieve pokemon by name
    """
    serializer_class = PokemonSerializer

    def get_object(self):
        data = self.request.GET
        if 'name' in data:
            try:
                obj = Pokemon.objects.get(name=data['name'])
                return obj
            except:
                raise CustomAPIException("This pokemon does not exist", status_code=status.HTTP_404_NOT_FOUND)
        else:
            raise CustomAPIException("Please enter 'name' as parameter", status_code=status.HTTP_400_BAD_REQUEST)
