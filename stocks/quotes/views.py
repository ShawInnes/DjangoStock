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

    if request.method == "POST":
        ticker = request.POST['ticker']
        api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={api_key}')

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'ticker': 'Enter a ticker above...'})

    return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    return render(request, 'add_stock.html', {})
