from django.db import models


# Create your models here.
class BaseStats(models.Model):
    """
    Model for base stat values for this Pokémon.
    """
    name = models.CharField(max_length=50)
    effort = models.PositiveIntegerField()
    base_stat = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class PokemonSpecies(models.Model):
    """
    Pokémon Species forms the basis for at least one Pokémon
    """
    name = models.CharField(max_length=50)
    id_poke_api = models.PositiveIntegerField(unique=True)


class EvolutionChain(models.Model):
    """
    Model for detail evolution conditions for each as well as Pokémon
    they can evolve into up through the hierarchy.
    """
    evolves_to = models.ForeignKey(PokemonSpecies, related_name='species', on_delete=models.CASCADE, blank=True,
                                   null=True)
    evolves_from = models.ForeignKey("PokemonSpecies", on_delete=models.CASCADE, blank=True, null=True)
    id_poke_api = models.PositiveIntegerField()


class Pokemon(models.Model):
    """
    Model for Pokemon
    """
    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    height = models.DecimalField(max_digits=6, decimal_places=3)
    base_stats = models.ManyToManyField(BaseStats)
    evolution = models.ForeignKey(EvolutionChain, on_delete=models.CASCADE)
    id_poke_api = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.name
