from django.shortcuts import render
import environ

ROOT_DIR = environ.Path(__file__) - 3
env = environ.Env()
env_file = str(ROOT_DIR.path('.env'))
env.read_env(env_file)

api_key = env('API_KEY')


def home(request):
    import requests
    import json

    api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/aapl/quote?token=' + api_key)

    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Error..."

    return render(request, 'home.html', {'api': api})


def about(request):
    return render(request, 'about.html', {})
