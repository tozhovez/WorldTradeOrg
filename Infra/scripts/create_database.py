
import os, sys
import subprocess
import yaml

from PyInquirer import prompt
from postgres_client import PostgresClient


def load_config_from_yaml(filename):
    with open(filename, "r", encoding='utf-8') as fd_reader:
        return yaml.full_load(fd_reader)


configs_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'postgres_schemas'))


pg_client = PostgresClient(dsn=os.getenv(
    'POSTGRES_URL',
    "postgres://docker:docker@localhost:5222/postgres"
    ))

questions = [{
    'type': 'list',
    'name': 'file',
    'message': 'Choose schema file',
    'choices': [*os.listdir(configs_dir)],
}]

answers = prompt(questions)

if not answers:
    sys.exit(0)


db_name = answers['file'].split('.')[0]

if pg_client.create_db(db_name, 'docker') is True:
    pg_url = str(f"postgres://docker:docker@localhost:5222/{db_name}")

    with open(os.path.join(configs_dir, answers['file']), 'r') as f:
        query = f.read()
        subprocess.run(["psql", pg_url, "--quiet", "-c", query])
