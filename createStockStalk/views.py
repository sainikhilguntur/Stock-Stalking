from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StockStalkSerializer
from .models import StockStalk
import requests
from django.core.mail import send_mail
from django.conf import settings

# Registers a new stalk.
# Stalk object includes three fields: stock_ticker, target_stock_price, email_to_notify 
@api_view(['PUT'])
def registerSS(request):
    requestData = request.data
    stockStalk = StockStalk.objects.create(
        stock_ticker = requestData['stock_ticker'],
        target_stock_price = requestData['target_stock_price'],
        email_to_notify = requestData['email_to_notify']
    )
    serializer = StockStalkSerializer(stockStalk, many=False)
    return Response(serializer.data)

# For every stalk available in the database, verifies with the latest stock price.
# If target stock price is reached, sends email to the specified email. 
@api_view(['GET'])
def monitorSS(request):
    # Get all stalk objects from database
    serializer = StockStalkSerializer(StockStalk.objects.all(), many=True)

    # Extract Stalk information into a dictionary
    stockTickers = { stock['stock_ticker']: (stock['target_stock_price'], stock['email_to_notify']) for stock in serializer.data}
    
    res = {}
    # Run verification for each stalk
    for stockTicker, stockInfo in stockTickers.items():
        # API Key for polygon 
        api_key = "iIfgNB7QSkAIr17RS_U4VTd8ImP8BouT"
        try:
            # REST API call for polygon. To retrieve stock latest stock price
            base_url = f'https://api.polygon.io/v2/aggs/ticker/{stockTicker}/prev?adjusted=true&apiKey={api_key}'
            data = requests.get(base_url).json()
            if 'results' in data:
                # Verify if current stock price is more than target price
                if data['results'][0]['vw'] > float(stockInfo[0]):
                    # Send Email
                    subject = 'Hurray!! your target price reached now go and sell your stocks'
                    message = f'Target Price of {stockInfo[0]} reached for Stock - {stockTicker}'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [stockInfo[1]]
                    send_mail(subject, message, from_email, recipient_list)
                    # Store the result in response
                    res[stockTicker]= f'Target Price of {stockInfo[0]} reached for Stock - {stockTicker} go ahead and sell your stocks!' + "\n"
                else:
                    res[stockTicker] = f'Target Price of {stockInfo[0]} not reached for Stock - {stockTicker} wait up!!' + "\n"
            else:
                res[stockTicker]= f"Not able to find info for stock - {stockTicker}" + "\n"

        except requests.exceptions.RequestException as e:
            res[stockTicker]= f"Error fetching stock price for the stock - {stockTicker}" + "\n"

    return Response(res)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': 'monitorStalk/',
            'Method': 'GET',
            'Body': None,
            'Description': "A call for this API will do one check for every stalk that's available in the database"
        },
        {
            'Endpoint': '/registerStalk',
            'Method': 'POST',
            'Body': None,
            'Description': 'An API call to register the stock option along with email needed for montoring the stock'
        }
    ]
    return Response(routes)