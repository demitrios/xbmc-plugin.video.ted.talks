import urllib
from url_constants import URLTED, URLSEARCH
# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions as xbmc_common
import re

__results_count_re__ = re.compile(r'.*\d+ - (\d+) of (\d+) results.*')

class Search:

    def __init__(self, get_HTML):
        self.get_HTML = get_HTML

    def get_talks_for_search(self, search_string, page_index):
        '''
        Yields number of results left to show after this page,
        then tuples of title, link, img for results on this page.
        '''
        # TODO Read result count and use for paging control

        search_string = urllib.quote_plus(search_string)
        html = self.get_HTML(URLSEARCH % (search_string, page_index))

        yield self.results_remaining(html)

        results = xbmc_common.parseDOM(html, 'article', {'class': 'm1 search__result'})
        print results
        for result in results:
            header = xbmc_common.parseDOM(result, 'h3')[0]
            title = xbmc_common.parseDOM(header, 'a')[0].strip()
            url = URLTED + xbmc_common.parseDOM(header, 'a', ret='href')[0]
            img = xbmc_common.parseDOM(result, 'img', ret='src')[0]
            yield title, url, img

    def results_remaining(self, html):
        search_results = xbmc_common.parseDOM(html, 'div', {'class': 'heading search__results__heading'})
        if search_results:
            results_count_matches = __results_count_re__.findall(search_results[0])
            if results_count_matches:
                match = results_count_matches[0]
                return int(match[1]) - int(match[0])

        # We don't know so just make sure that it is positive so that we keep paging.
        return 1
