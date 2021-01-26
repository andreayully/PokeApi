from django.core.management.base import BaseCommand
from pokemon.models import *
import requests
import logging
import http.client
from requests.exceptions import HTTPError
import os


def generate_request(url):
    try:
        os.environ['no_proxy'] = '*'
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        return response.json()


def save_models(response_evolution_chain, response_pokemon, evolution_from_species):
    print("""*** saving pokemon information ***""")
    evolves_from = None
    if evolution_from_species:
        evolves_from, created_from = PokemonSpecies.objects.get_or_create(
            name=evolution_from_species['name'],
            id_poke_api=evolution_from_species['url'].split("/")[6])
        print("evolves from saved")
    if response_evolution_chain['chain']['evolves_to'][0]['evolves_to']:
        evolves_to_list = response_evolution_chain['chain']['evolves_to'][0]['evolves_to']
        evolves_to, created_to = PokemonSpecies.objects.get_or_create(
            name=evolves_to_list[0]['species']['name'],
            id_poke_api=evolves_to_list[0]['species']['url'].split("/")[6])
    else:
        evolves_to, created_to = PokemonSpecies.objects.get_or_create(
            name=response_evolution_chain['chain']['evolves_to'][0]['species']['name'],
            id_poke_api=response_evolution_chain['chain']['evolves_to'][0]['species']['url'].split("/")[6])
    print("evolves_to saved")
    evolution_chain, created_chain = EvolutionChain.objects.get_or_create(
        evolves_to=evolves_to,
        evolves_from=evolves_from,
        id_poke_api=response_evolution_chain['id'])
    print("evolution chain saved")
    print(response_pokemon['id'])
    pokemon, created_pokemon = Pokemon.objects.update_or_create(
        name=response_pokemon['name'],
        weight=response_pokemon['weight'],
        height=response_pokemon['height'],
        evolution=evolution_chain,
        id_poke_api=response_pokemon['id'],
    )
    print("pokemon saved")
    for stat in response_pokemon['stats']:
        base_stat, created = BaseStats.objects.get_or_create(
            name=stat['stat']['name'],
            effort=stat['effort'],
            base_stat=stat['base_stat'],
        )
        pokemon.base_stats.add(base_stat)
    print("stats saved")


class Command(BaseCommand):

    def handle(self, *args, **options):
        poke_api_url = "https://pokeapi.co/api/v2/{}"
        poke_species = poke_api_url.format("pokemon-species/{}/")
        pokemon_endpoint = poke_api_url.format("pokemon/{}/")
        poke_id = input('Enter Poke id: ')
        response_species = generate_request(poke_species.format(poke_id))
        response_pokemon = generate_request(pokemon_endpoint.format(poke_id))
        evolution_to = response_species['evolution_chain']
        evolution_from_species = response_species['evolves_from_species']
        response_evolution_chain = generate_request(evolution_to['url'])
        save_models(response_evolution_chain, response_pokemon, evolution_from_species)
        self.stdout.write(
            self.style.SUCCESS('Pokemon successfully stored "%s"' % response_pokemon['name'].capitalize()))
