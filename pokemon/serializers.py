from rest_framework import serializers
from pokemon.models import Pokemon, EvolutionChain, BaseStats, PokemonSpecies


class PokemonSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonSpecies
        fields = '__all__'


class EvolutionChainSerializer(serializers.ModelSerializer):
    evolves_to = PokemonSpeciesSerializer()
    evolves_from = PokemonSpeciesSerializer()

    class Meta:
        model = EvolutionChain
        fields = '__all__'


class BaseStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseStats
        fields = '__all__'


class PokemonSerializer(serializers.ModelSerializer):
    base_stats = BaseStatsSerializer(many=True)
    evolution = EvolutionChainSerializer()

    class Meta:
        model = Pokemon
        fields = '__all__'
