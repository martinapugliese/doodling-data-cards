from os import remove
import json
from google.cloud import storage


def main():

    # Download the blobs one at a time to file, put in dict and remove file
    # existing_blobs = bucket.list_blobs()
    #
    # all_blobs = []
    # i = 0
    # for blob in existing_blobs:
    #     blob.download_to_file(open(blob.name, 'wb'))
    #     all_blobs.append(json.load(open(blob.name, 'r')))
    #     remove(blob.name)
    #     i += 1
    #     if i == 50:
    #         break
    #
    # json.dump(all_blobs, open('all_blobs.json', 'w'))




if __name__ == "__main__":

    # Client and bucket to connect to Google Storage
    client = storage.Client()
    bucket = client.get_bucket('tweepy-trump-tweets')

    main()
