import json
import logging
from urllib.parse import urlparse

from fp.fp import FreeProxy
from rank_analysis.google_rank.google_search_proxy.search_ import search
from tldextract import tldextract
import logging  # NoQa

logging.basicConfig()


def get_domain_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


def get_proxy():
    return FreeProxy(rand=True).get()


def get_domain(url):
    """
    extract domain from url
    """

    ext_ = tldextract.extract(url)
    return ext_.domain


def google_rank(input_):
    """
    get google rank for each invite
    """
    output = {}
    try:
        for record_ in input_:
            website_name = get_domain(record_["url"])
            website_name = website_name.lower()
            for keyword_ in record_["keywords"]:
                # os.environ['http_proxy'] = get_proxy()
                keyword_ = keyword_.strip()
                output[keyword_] = {}
                counter_ = 0
                last_url_domain = ""

                for url in search(keyword_, num=110, pause=20):
                    url_domain = get_domain_url(url)
                    counter_ += 1
                    if last_url_domain == url_domain:
                        counter_ -= 1
                    if website_name in url.lower():
                        output[keyword_] = {"url": url, "rank": counter_}
                        break
                    last_url_domain = url_domain
                with open("output.json", "w") as outfile:
                    json.dump(output, outfile, indent=4)
                logging.info(f"processed: {keyword_}")
    except Exception as e:
        logging.info("error", exc_info=e)
    finally:
        return output
