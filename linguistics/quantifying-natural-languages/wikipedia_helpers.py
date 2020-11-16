import wikipedia


def get_pages_content(queries, lang_code='en'):
    """
    Use the wikipedia library to request the content of pages from Wikipedia.
    Results limited to 500 per query as this seems to be the maximum.

    - queries: a list of string queries to request pages for
    - lang_code: the ISO language code of the Wikipedia to use
                 (default is English)

    Return dict {page_title: page_content}.
    """

    wikipedia.set_lang(lang_code)
    contents = {}

    print 'Requesting pages on the %s Wikipedia ...' % lang_code

    for query in queries:
        count = 0
        for page_title in wikipedia.search(query, results=500):

            # Exception could be a disambiguation but also other things
            try:
                page = wikipedia.page(page_title)
                contents[page_title] = page.content
            except Exception:
                pass

            if count % 100 == 0:
                print query, count

            count += 1

    return contents


def get_random_pages_content(lang_code='en', num_pages=500):
    """
    Use the wikipedia library to request the content of random pages
    from Wikipedia.

    - lang_code: the ISO language code of the Wikipedia to use
                 (default is English)
    - num_pages: num of pages to request, defaults to 500

    Return dict {page_title: page_content}.
    """

    wikipedia.set_lang(lang_code)
    contents = {}

    print 'Requesting random pages on the %s Wikipedia ...' % lang_code

    count = 0
    for page_title in wikipedia.random(pages=num_pages):

        # Exception could be a disambiguation but also other things
        try:
            page = wikipedia.page(page_title)
            contents[page_title] = page.content
        except Exception:
            pass

        if count % 100 == 0:
            print count

        count += 1

    return contents
