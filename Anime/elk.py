import os
import re
from datetime import datetime
from elasticsearch import Elasticsearch

# Elasticsearch credentials and endpoint
elastic_cloud_endpoint = "https://81d9dc1bd63d45f497a94a307677e119.us-central1.gcp.cloud.es.io:443"
username = "elastic"
password = "sRlHJmrEOwXse5zexTPKA8yu"

# Initialize the Elasticsearch client
es = Elasticsearch(
    [elastic_cloud_endpoint],
    basic_auth=(username, password),
)

# Define index configuration
index_name = "index"  # Replace with your actual index name

# Path to the log file
log_file_path = os.path.join(os.path.dirname(__file__), 'logs', 'app.log')

def parse_log_line(line):
    log_pattern = re.compile(
        r'^(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:\d{2}) '
        r'\[(?P<thread>[^\]]+)\] (?P<level>\w+)  '
        r'(?P<logger>[^\s]+) - (?P<message>.*)$'
    )

    match = log_pattern.match(line)
    if match:
        log_data = match.groupdict()
        log_data['timestamp'] = datetime.strptime(log_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')
        return log_data
    else:
        return {"message": line.strip()}

# Read log file and index each line as a document in Elasticsearch
with open(log_file_path, 'r') as log_file:
    for doc_id, line in enumerate(log_file, start=1):
        doc_body = parse_log_line(line)
        res = es.index(index=index_name, id=doc_id, body=doc_body)
        print(res)

# Close the connection
es.close()
