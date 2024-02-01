import requests
from prefect import task, flow

@task
def make_request():
    response = requests.get('http://52.200.184.250/monitorStalk/')
    return response.text

@task
def process_response(response_text):
    print("Received response:", response_text)

@flow
def serverMonitoring():
    response = make_request()
    processed_response = process_response(response)

serverMonitoring()