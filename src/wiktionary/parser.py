#!/usr/bin/python
# -*- coding: ascii -*-

import tomllib 
import os
import json
from src.utils import get_project_root

ROOT_DIR = get_project_root()
print(ROOT_DIR)

config = {}
with open(f"{ROOT_DIR}/config.toml", mode="rb") as fp:
    config = tomllib.load(fp)

def get_meaning(senses):
    print(f"here are the senses: {senses}")
    for sense in senses:
        try:
            links = sense['links']
        except KeyError:
            print("no links")
        glosses = sense['glosses']
        print (f"links: {links}\nglosses: {glosses}")


def parse_word_and_etymology(entry):
    if "etymology_text" in entry:
        return f"{entry['word']}, from: {entry['etymology_text']}"
    else:
        return entry['word']

def parse_english():
    pass

def parse_yiddish():
    pass

def flag_if_nonstandard(entry, output_file):
    print(entry)
    if any(filter(lambda x: 'Unpointed' in x, entry['links'])) or 'nonstandard' in entry['tags']:
        print("were here")
        with open(output_file, "a") as f:
            f.writelines(f"Could not parse nonstandard entry {entry['word']}\n")

def write_entry(data, language):
    with open(f"{config['data']['wiktionary_output_data_directory']}/{language}.txt", 'a') as outfile:
        outfile.writelines(f"{data}\n")



if __name__ == '__main__':

    wiktionary_data_filename = config['data']['wiktionary_filename']
    print(wiktionary_data_filename)
    with open(f"{ROOT_DIR}/{wiktionary_data_filename}", encoding="utf-8") as data_file:
        for line in data_file:
            data = json.loads(line)
            print(f"\n\n{data}\n\n")
            print(f"\n--- processing new word: {parse_word_and_etymology(data)}---")
            get_meaning(data['senses'])
            input("push enter")
