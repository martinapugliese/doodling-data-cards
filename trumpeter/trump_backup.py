import json
import os
from datetime import datetime
import multiprocessing
import re
import operator

import spacy
import textacy


# Global vars
en_lang_model = spacy.load('en')     # English spaCy language model


class TweetingTrump(object):
    """
    Class for the tweeting Donald Trump.
    Constructor takes the folder where tweets files are stored.
    Class attributes (built) are the list of tweets objects and the
    textacy corpus of their texts.
    """

    def __init__(self, tweets_folder):

        self.tweets = self._read_tweets(tweets_folder)
        self.corpus = self._build_corpus()

    def give_me_tweets_infos(self):
        """Give some meta information on the tweets.

        Returns:
            dict with
                - number of tweets,
                - date of first tweet (UTC time as per Twitter)
                - date of last tweet (UTC time as per Twitter)
                - timespan of tweets in days
                - number of quoted tweets
                - counts of tweets for each (Twitter-detected) languages

        Notes:
            - coordinate/geo/place are nullable so not used

        """

        dates = [datetime.strptime(tweet['created_at'],
                                   '%a %b %d %H:%M:%S +0000 %Y')
                 for tweet in self.tweets]

        count_quoted = 0
        langs_counts = {}
        num_replies = 0
        for tweet in self.tweets:

            if 'quoted_status' in tweet:
                count_quoted += 1

            lang = tweet['lang']
            langs_counts[lang] = langs_counts.get(lang, 0) + 1

            if tweet['in_reply_to_user_id']:
                num_replies += 1

        return {
            'num_tweets': len(self.tweets),
            'min_date': min(dates),
            'max_date': max(dates),
            'timespan_days': (max(dates) - min(dates)).days,
            'num_quoted': count_quoted,
            'languages_counts': langs_counts
        }

    def measure_time_prolificity(self):
        """
        Measures the tweeting prolificity per day.

        Returns:
            - list of tuples sorted (by day asc) from dict {day: number tweets}
            - list of tuples sorted (by hour of day asc) from dict
              {hour of day: number tweets}
        """

        days_counts = {}
        hour_day_counts = {}
        for tweet in self.tweets:
            dttime = datetime.strptime(
                tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

            tweet_date = dttime.date()
            tweet_time = dttime.time()

            days_counts[tweet_date] = days_counts.get(tweet_date, 0) + 1
            hour_day_counts[tweet_time.hour] = \
                hour_day_counts.get(tweet_time.hour, 0) + 1

        return sorted(days_counts.items(), key=operator.itemgetter(0)), \
               sorted(hour_day_counts.items(), key=operator.itemgetter(0))

    def count_entities(self):
        """
        Count the occurrences of entities
        (we consider only hashtags, mentions, URLs).

        Returns a dict with
            - count of tweets containing at least one hashtag
            - count of tweets containing at least one mention
            - count of tweets containing at least one URL
            - count of occurrences for each hashtag
              (list of tuples sorted by value desc)
            - count of occurrences for each mention
              (list of tuples sorted by value desc)

        """

        count_tweets_hashtags = 0
        count_tweets_mentions = 0
        count_tweets_urls = 0
        hashtags_d, mentions_d = {}, {}

        for tweet in self.tweets:

            if len(tweet['entities']['hashtags']) > 0:
                count_tweets_hashtags += 1
                for item in tweet['entities']['hashtags']:
                    ht = item['text'].lower()
                    hashtags_d[ht] = hashtags_d.get(ht, 0) + 1

            if len(tweet['entities']['user_mentions']) > 0:
                count_tweets_mentions += 1
                for item in tweet['entities']['user_mentions']:
                    m = item['screen_name']
                    mentions_d[m] = mentions_d.get(m, 0) + 1

            if len(tweet['entities']['urls']) > 0:
                count_tweets_urls += 1

        return {
            'num_tweets_with_hashtags': count_tweets_hashtags,
            'num_tweets_with_mentions': count_tweets_mentions,
            'num_tweets_with_urls': count_tweets_urls,
            'hashtags_counts': sorted(hashtags_d.items(),
                                      key=operator.itemgetter(1),
                                      reverse=True),
            'mentions_counts': sorted(mentions_d.items(),
                                      key=operator.itemgetter(1),
                                      reverse=True)
        }

    def extract_information(self):
        """Extract information from tweets text.

        lowers case

        Return:
            -
            -
            -

        """

        token_freqs = {}
        named_entities = {}
        bigrams = {}
        for doc in self.corpus:

            doc_bag = doc.to_bag_of_terms(as_strings=True,
                                          ngrams=1,
                                          named_entities=False,
                                          filter_stops=True,
                                          normalize='lemma')
            doc_bigrams = textacy.extract.ngrams(doc, 2, filter_stops=False)
            doc_named_entities = textacy.extract.named_entities(doc)

            for item in doc_bag:
                token_freqs[item] = token_freqs.get(item, 0) + 1

            for item in doc_bigrams:
                item_u = item.lower_
                bigrams[item_u] = bigrams.get(item_u, 0) + 1

            for item in doc_named_entities:
                item_u = item.lower_
                named_entities[item_u] = named_entities.get(item_u, 0) + 1

        return sorted(token_freqs.items(),
                      key=operator.itemgetter(1),
                      reverse=True), \
               sorted(bigrams.items(),
                      key=operator.itemgetter(1),
                      reverse=True), \
               sorted(named_entities.items(),
                      key=operator.itemgetter(1),
                      reverse=True)


    def _read_tweets(self, folder):
        """Read tweets from files in folder, return list of."""

        tweets = []
        for filename in os.listdir(folder):
            if filename != '.DS_Store':   # might not be there
                tweets.append(json.load(open(folder + filename, 'r')))

        return tweets


    def _build_corpus(self):
        """Builds a textacy Corpus with the 'en' spaCy language model,
        adding all tweets' texts (fixing potential UnicodeEncode errors
        beforehand, only normalisation we do) in parallel over the number of machine cores.

        Return:
            the textacy corpus with all docs

        """

        c = textacy.corpus.Corpus(en_lang_model)

        c.add_texts(
            [textacy.preprocess.fix_bad_unicode(tweet['text'])
             for tweet in self.tweets],
            n_threads=multiprocessing.cpu_count(),
            batch_size=100)

        return c

    def _isolate_special_tokens(self, starting_char, lower=True):
        """
        Performs a bespoke tokenisation which considers everything
        alphanumeric after the starting_char and lowers the case if desired.

        This is useless as tweet comes with the hashtags and
        mentions on separate fields. Keeping this for nostaling reasons.
        """

        # Filter docs containing tokens with a special char
        filtered_docs = \
            list(self.corpus.get(lambda doc: starting_char in doc.text))

        # Build corpus with these docs
        selected_corpus = textacy.corpus.Corpus(en_lang_model)
        selected_corpus.add_texts(
            [doc.text for doc in filtered_docs],
            n_threads=multiprocessing.cpu_count(),
            batch_size=100)

        # Builds the list of these special tokens, lowering case if desired
        special_tokens = []
        for doc in selected_corpus:
            text = doc.text.lower() if lower is True else doc.text
            special_tokens += re.findall(starting_char + '[a-zA-Z0-9]+', text)

        return special_tokens
