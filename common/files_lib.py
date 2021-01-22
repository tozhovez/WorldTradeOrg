import asyncio
import json
import csv
import aiofiles
import yaml


def load_config_from_yaml(filename):
    with open(filename, "r", encoding='utf-8') as fd_reader:
        return yaml.full_load(fd_reader)


async def async_load_config_from_yaml(filename):
    async with aiofiles.open(filename, "r", encoding='utf-8') as fd_reader:
        data = yaml.full_load(fd_reader)
        return data


def file_read(filename):
    with open(filename, "r", encoding="utf-8") as file_reader:
        for row in file_reader.read().split():
            yield row


async def async_file_read_csv(filename):
    async with aiofiles.open(filename,"r",encoding="utf-8", newline='') as csvfile:
        print((csvfile))
        reader = csv.DictReader(csvfile, restval=None)
        return reader



def file_read_csv(filename):
    with open(filename,"r",encoding="utf-8", newline='') as csvfile:
        reader = iter(csv.DictReader(csvfile, restval=None))
        for row in reader:
            yield row


async def async_read_from_csv_file(filename):
    async with aiofiles.open(filename, "r", encoding="utf-8") as file_reader:
        for row in file_reader.read().split():
            yield row


async def async_write_to_json_file(data_object, file_name):
    async with aiofiles.open(file_name, "w") as outfile:
        print(f'Writing "{data_object}" to "{file_name}"...')
        await outfile.write(json.dumps(data_object, indent=4))







