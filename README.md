## PokeApi
Django application that consults the information of the [PokeApi](https://pokeapi.co/)  
Bring information from the pokeapi with a custom django command and exposes a service to list the pokemon stored with their characteristics 
like name, base stats, height, weight and evolutions.

### To run locally
* pre requirements Python 3.+ and Virtualenv
1. Create virtual environment and activate environment  
`python3 -m venv myvenv`  
`source venv/bin/activate`

2. Clone repository `git clone https://github.com/andreayully/PokeApi.git`

3. Install requirements `pip install -r requirements.txt`

4. Runserver ` python manage.py runserver`

### Command to store PokeApi information
Requires pokemon ID  
`python manage.py poke_api_data`
~~~
Enter Poke id: 5  
*** saving pokemon information ***
evolves from saved
evolves_to saved
evolution chain saved
pokemon saved
stats saved
Pokemon successfully stored "Charmeleon"
~~~

### Swagger generator
For documentation  
http://localhost:8000/swagger/  
http://localhost:8000/redoc/#tag/pokemon  

### Postman collection
https://www.getpostman.com/collections/7de1acd33198a3baa034

### Feature
* Django 3.1.5
* Django Rest-Framework 3.12.2
* PokeApi V.2
