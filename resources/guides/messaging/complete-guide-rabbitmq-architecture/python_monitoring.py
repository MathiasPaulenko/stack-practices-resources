"""RabbitMQ monitoring via Management API.

Fetches queue stats and checks key metrics.
Run: python python_monitoring.py
"""
import requests


def get_queue_stats(host="localhost", port=15672, user="admin", password="password"):
    """Fetch queue statistics from the RabbitMQ Management API."""
    url = f"http://{host}:{port}/api/queues"
    response = requests.get(url, auth=(user, password))
    response.raise_for_status()
    return response.json()


def check_alerts(queues, thresholds=None):
    """Check queue metrics against alert thresholds."""
    if thresholds is None:
        thresholds = {
            "messages": 10000,
            "messages_unacknowledged": 5000,
            "consumers": 1,
        }

    alerts = []
    for q in queues:
        name = q["name"]
        messages = q.get("messages", 0)
        unacked = q.get("messages_unacknowledged", 0)
        consumers = q.get("consumers", 0)

        if messages > thresholds["messages"]:
            alerts.append(f"ALERT: {name} queue depth {messages} > {thresholds['messages']}")
        if unacked > thresholds["messages_unacknowledged"]:
            alerts.append(f"ALERT: {name} unacked {unacked} > {thresholds['messages_unacknowledged']}")
        if consumers < thresholds["consumers"]:
            alerts.append(f"ALERT: {name} has {consumers} consumers (min: {thresholds['consumers']})")

    return alerts


def print_stats(queues):
    """Print queue statistics."""
    for q in queues:
        print(f"Queue: {q['name']}")
        print(f"  Messages: {q.get('messages', 0)}")
        print(f"  Consumers: {q.get('consumers', 0)}")
        print(f"  Unacked: {q.get('messages_unacknowledged', 0)}")
        print()


if __name__ == "__main__":
    try:
        queues = get_queue_stats()
        print_stats(queues)
        alerts = check_alerts(queues)
        if alerts:
            print("=== ALERTS ===")
            for alert in alerts:
                print(alert)
        else:
            print("No alerts — all queues within thresholds.")
    except requests.exceptions.ConnectionError:
        print("Could not connect to RabbitMQ Management API at localhost:15672")
        print("Start RabbitMQ with management plugin enabled.")
