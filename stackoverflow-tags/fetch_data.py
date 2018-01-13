# Script to fetch Stack Overflow (SO) data

from stackapi import StackAPI
import json
from os import environ

# GLOBAL VARS AND SETTINGS

key = environ['PYVERFLOW_KEY']               # SO API registered key
data_folder = 'data/'

so = StackAPI('stackoverflow', key=key)      # object to query SO


# NOTE: to see the quota of requests remaining you got, run
# r['quota_remaining'] with r being the last response object (see below)
# initial quota is 10000


def fetch_and_organise_SO_tags_data(filename, count_printing=50):
    """
    Query the Stack Overflow API, organise the data and write on filename file.
    The max results allowed per page is 100 and each page is an API hit.
    A total of 10000 hits is allowed by the API.

    Procedure is this:
        1. Request tags (100 - max allowed) per page,

    Pass:
        - the filename over which to write
        - the how often you want print to happen on stdout (for seeing where you are)
    """

    # Request tags endpoint: standard sorting is by popularity
    # Setting to the max of results per page allowed (100) and request 2 pages
    so.page_size = 100
    so.max_pages = 1
    r = so.fetch('tags')

    # Start the data dict with the retrieved data
    tags_data = {t['name']: t for t in r['items']}

    # Add fields for the tag creation date and list of synonyms
    for t in tags_data:
        tags_data[t].update({'creation_date': None, 'synonyms': []})

    # Query for the date of the first questions created with each tag
    # for creation date of the tag, update the dict
    # set to 1 page per tag
    so.max_pages = 1
    count = 0
    t_timestamps = {},
    for t in tags_data:
        r = so.fetch('search',
                     tagged=t,
                     sort='creation',
                     order='asc',
                     pagesize=1)
        tags_data[t]['creation_date'] = r['items'][0]['creation_date']
        count += 1
        if count % count_printing == 0:
            print('creation date', count, 'of', len(tags_data))

    # Query for the synonyms of each tag
    tags_syns_items = []
    for count in range(0, len(tags_data) - 20 + 1, 20):
        print('synonyms', count, 'of', len(tags_data))
        tags_syns_items += so.fetch(
            'tags/{tags}/synonyms',
            tags=list(tags_data.keys())[count:count + 20])['items']

    for item in tags_syns_items:
        tags_data[item['to_tag']]['synonyms'].append(item['from_tag'])

    # Dump the built dict to file
    f = open(filename, 'w')
    json.dump(tags_data, f, indent=4)
    f.close()

    return


if __name__ == "__main__":

    # Fetch data from the SO API
    fetch_and_organise_SO_tags_data(data_folder + 'tags_data_12Jan.json')


# # Request questions, from old to newer
# questions_r = so.fetch('questions', order='asc', sort='creation')
