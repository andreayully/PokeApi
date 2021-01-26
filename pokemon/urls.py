from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from pokemon.views import PokemonListCreateView, PokemonRetrieveView

urlpatterns = {
    path('pokemon/', PokemonListCreateView.as_view(), name="create"),
    path('pokemon/get_by_name/', PokemonRetrieveView.as_view(), name="retieve"),
}
urlpatterns = format_suffix_patterns(urlpatterns)
