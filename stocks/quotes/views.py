from django.shortcuts import render, redirect
import environ
from .models import Stock
from .forms import StockForm

from django.contrib import messages

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
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, (f"Stock {form.cleaned_data['ticker']} has been added"))
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()
        tickers = []
        for ticker_item in ticker:
            api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/{str(ticker_item)}/quote?token={api_key}')

            try:
                api = json.loads(api_request.content)
                tickers.append(api)
            except Exception as e:
                tickers = "Error..."

    return render(request, 'add_stock.html', {'tickers': tickers})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, (f"Stock {item} has been deleted"))
    return redirect(delete_stock)


def delete_stock(request):
    tickers = Stock.objects.all()
    return render(request, 'delete_stock.html', {'tickers': tickers})
