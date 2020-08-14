from django.shortcuts import render
from django.http import HttpResponse
import requests

def request_pokemons(url, offset):
	args= {'offset':offset} if offset else {}
	response= requests.get(url, params=args)
	if response.status_code==200:
		payload =response.json()
		results= payload.get('results', [])
		return results

def sprites(url):
	response= requests.get(url)
	if response.status_code == 200:
		payload =response.json()
		results= payload.get('sprites', [])
		sprite = results['front_default']
		return sprite

def get_id_pokemon(url):
    response = requests.get(url)
    results  = '' 
    data  = response.json()
    results = data
    return  results

def home(request):
	limit = 10
	if request.method == 'POST':
		limit = request.POST.get('limit')
		print(limit)
	pokemons = request_pokemons('https://pokeapi.co/api/v2/pokemon/?limit={}'.format(limit),0)
	dic = {}
	results = {}
	contador = 0
	if pokemons:
		for pokemon in pokemons:
			contador=contador+1
			name= pokemon['name']
			url= pokemon['url']
			id_ = get_id_pokemon(url)
			id_pokemon = id_['id']
			sprite = sprites(url)
			dic = { 
			'name':name, 
			'sprite':sprite, 
			'url':url, 
			'id_pokemon':id_pokemon}

			results[contador]= dic		

	return render (request, 'home.html',{
		'results':results
		})

def get_detalles(url):
	response= requests.get(url)
	if response.status_code==200:
		payload =response.json()
		results= payload.get('sprites', [])
		return payload
	
def detalles_pokemon(requests, id_pokemon,nombre_pokemon):
	url='http://pokeapi.co/api/v2/pokemon/{}/'.format(id_pokemon)
	detalles=get_detalles(url)
	nombre=nombre_pokemon
	weight=detalles.get('weight')
	height=detalles.get('height')
	types= detalles.get('types', [])
	abilities=detalles.get('abilities', [])
	moves=detalles.get('moves', [])
	tipos={}
	dic_tipo={}
	habilidades={}
	movimientos={}
	contador=0
	if types:
		for j in types:
			contador=contador+1
			tipo=j['type']
			nombre_tipo=tipo['name']
			url_tipo=tipo['url']
			id_tipo = get_id_pokemon(url)
			tipos= {'tipo':nombre_tipo, 'id_tipo':id_tipo}
			dic_tipo[contador]=tipos

	if abilities:
		for k in abilities:
			contador=contador+1
			habilidad=k['ability']
			habilidad=habilidad['name']
			habilidades[contador]= habilidad

	if moves:
		for l in moves:
			contador=contador+1
			movimiento=l['move']
			movimiento=movimiento['name']
			movimientos[contador]= movimiento

	sprite=sprites(url)

	return render (requests, 'detalles_pokemon.html',{
		'nombre':nombre, 
		'weight':weight, 
		'sprite':sprite, 
		'height':height, 
		'tipos':dic_tipo, 
		'habilidades': habilidades, 
		'movimientos':movimientos,
		})

def tipos_pokemon(request, id_tipo):

	#url = 'https://pokeapi.co/api/v2/type/?limit=1&offset=1'
	limit = 5
	#if request.method == 'POST':
	#	limit = request.POST.get('limit')


	url='http://pokeapi.co/api/v2/type/{}'.format(id_tipo)
	detalles=get_detalles(url)
	types_pokemons=detalles.get('pokemon', [])
	dic={}
	results={}
	
	contador = 0

	if types_pokemons:
		for pokemon in types_pokemons:
			contador=contador+1
			pokemon=pokemon['pokemon']
			name=pokemon['name']
			url= pokemon['url']
			id_ = get_id_pokemon(url)
			id_pokemon = id_['id']
			#print(id_pokemon)
			sprite =sprites(url)
			dic = { 'name':name, 'sprite':sprite,'id_pokemon':id_pokemon}
			results[contador]= dic
			print(contador)
			if contador == limit:
				print('Break!')
				break

	return render (request, 'home.html',{'results':results})