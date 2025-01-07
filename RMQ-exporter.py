#This code snippet does the following:
#Import necessary libraries: os, time, requests for interacting with the system and the RabbitMQ API, and prometheus_client for creating and exporting Prometheus metrics.
#Retrieve environment variables:  The code uses os.environ.get() to fetch the RabbitMQ host, username, and password from environment variables, allowing for easy configuration across different deployments.
#Define Prometheus metrics
#Constructs the URL to the RabbitMQ API endpoint for queues.
#Calls get_queue_data() to fetch the queue data.
#Starts the Prometheus HTTP server on port 8000, making the metrics accessible.
#Enters a loop to continuously update the metrics every 15 seconds.

import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Environment variables
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'guest')
RABBITMQ_API_PORT = os.environ.get('RABBITMQ_API_PORT', '15672')

# Prometheus metrics
rabbitmq_individual_queue_messages = Gauge(
    'rabbitmq_individual_queue_messages',
    'Total count of messages in a queue',
    ['host', 'vhost', 'name']
)
rabbitmq_individual_queue_messages_ready = Gauge(
    'rabbitmq_individual_queue_messages_ready',
    'Number of messages ready for delivery in a queue',
    ['host', 'vhost', 'name']
)
rabbitmq_individual_queue_messages_unacknowledged = Gauge(
    'rabbitmq_individual_queue_messages_unacknowledged',
    'Number of unacknowledged messages in a queue',
    ['host', 'vhost', 'name']
)

def get_queue_data():
    """Retrieves queue data from RabbitMQ API."""
    try:
        response = requests.get(
            f'http://{RABBITMQ_HOST}:{RABBITMQ_API_PORT}/api/queues',
            auth=(RABBITMQ_USER, RABBITMQ_PASSWORD)
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from RabbitMQ API: {e}")
        return []

def update_metrics():
    """Updates Prometheus metrics with queue data."""
    queue_data = get_queue_data()
    for queue in queue_data:
        vhost = queue['vhost']
        name = queue['name']
        rabbitmq_individual_queue_messages.labels(
            host=RABBITMQ_HOST, vhost=vhost, name=name
        ).set(queue['messages'])
        rabbitmq_individual_queue_messages_ready.labels(
            host=RABBITMQ_HOST, vhost=vhost, name=name
        ).set(queue['messages_ready'])
        rabbitmq_individual_queue_messages_unacknowledged.labels(
            host=RABBITMQ_HOST, vhost=vhost, name=name
        ).set(queue['messages_unacknowledged'])

if __name__ == '__main__':
    # Start Prometheus HTTP server
    start_http_server(8000)
    print("Prometheus exporter started on port 8000")

    # Update metrics periodically
    while True:
        update_metrics()
        time.sleep(15)  # Update every 15 seconds
