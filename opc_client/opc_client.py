from datetime import datetime
import time
import logging

# import library for OPC
import schedule
from opcua import Client

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_opcua_client(server_url):
    client = Client(server_url)
    try:
        client.connect()
        logging.info("Connected to OPC UA Server.")
        return client
    except Exception as e:
        logging.error(f"Error connecting to server: {e}")
        return None

def read_multiple_tags_and_store(client, node_ids):
    if client is None:
        return None

    results = []

    # Read OPC tags and append to results
    for node_id in node_ids:
        try:
            node = client.get_node(node_id)
            tag_value = node.get_value()
        except Exception as e:
            logging.error(f"Error reading node {node_id}: {e}")
            tag_value = 0
        results.append(tag_value)

    return results

def scheduled_job(client, node_ids):
    values = read_multiple_tags_and_store(client, node_ids)
    keys = ['Tag1', 'Tag2', 'Tag3', 'Tag4']
    result = {k:v for (k,v) in zip(keys, values)}
    print(result)

if __name__ == '__main__':

    server_url = "opc.tcp://localhost:49320" # change to your OPC server IP and Port
    node_ids = ["ns=2;s=Channel1.Device1.Tag1",
                "ns=2;s=Channel1.Device1.Tag2",
                "ns=2;s=Channel1.Device1.Tag3",
                "ns=2;s=Channel1.Device1.Tag4",]

    client = setup_opcua_client(server_url)

    if client:
        schedule.every(2).seconds.do(scheduled_job, client=client, node_ids=node_ids)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        finally:
            client.disconnect()
    else:
        logging.error("Failed to connect to OPC UA server.")
