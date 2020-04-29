from bs4 import BeautifulSoup as Soup
import re, urllib.request
from pathlib import Path
import requests


def removeWeirdChars(text0):
    weridPatterns = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               u"\u2069"
                               u"\u2066"
                               u"\u200c"
                               u"\u2068"
                               u"\u2067"
                               "]+", flags=re.UNICODE)
    return weridPatterns.sub(r'', text0)


def get_html_files(path: str) -> list:
    files_path: list = list(Path(path).glob('*.html'))
    htmls = []
    for file in files_path:
        htmls.append(open(file, 'r').read())
    return htmls


def process_data(a_soup: Soup):
    my_dict = {}
    messages = a_soup.find_all('div', class_=['message default clearfix', 'message default clearfix joined'])
    for msg in messages:
        my_dict = extract_data(msg)


def extract_data(message):
    a_dict = {}
    # print(message)
    date, time = message.find('div', class_="pull_right date details").get('title').split()
    # if 'reply_to details' in message.attrs.values():
    is_reply = message.find('div',class_="reply_to details")
    if is_reply:
        is_reply = is_reply.find('a').get('href').split('_')[2]

    return a_dict


# dir_path = input()
# my_html = '\n'.join(get_html_files(dir_path))
# my_html = removeWeirdChars(my_html)
my_soup = Soup(open('messages34.html', 'r').read(), 'html.parser')
process_data(my_soup)
