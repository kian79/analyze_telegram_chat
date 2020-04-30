from bs4 import BeautifulSoup as Soup
import re, urllib.request
from pathlib import Path
import csv
from tqdm import tqdm


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
    print(len(htmls))
    return htmls


def process_data(a_list: list):
    my_list = []
    my_dict={}
    for i in tqdm(range(len(a_list))):
        a_soup = Soup(a_list[i],'html.parser')
        my_dict={}
        messages = a_soup.find_all('div', class_=['message default clearfix','message default clearfix joined'])
        username = ""
        for msg in messages:
            my_dict = extract_data(msg)
            if my_dict['user_id']:
                username = my_dict['user_id']
            else:
                my_dict['user_id'] = username
            my_list.append(my_dict)
    with open('tele_data.csv', 'a') as my_csv:
        my_writer = csv.DictWriter(my_csv, fieldnames=my_dict.keys())
        my_writer.writeheader()
        my_writer.writerows(my_list)


def extract_data(message):
    date, time = message.find('div', class_="pull_right date details").get('title').split()
    msg_id = message.get('id')[7:]
    is_reply = message.find('div', class_="reply_to details")
    if is_reply:
        is_reply = is_reply.find('a').get('href').split('_')[2][7:]

    text = message.find('div', class_='text')
    if not text:
        text = "NO TEXT"
    else:
        text=text.text
    user = message.find('div', class_="from_name")
    if user:
        user=user.text
    a_dict = dict(
        msg_id=msg_id,
        user_id=user,
        text=text,
        date=date,
        time=time,
        reply_to=is_reply
    )

    return a_dict


dir_path = input()
print(0)
my_html = get_html_files(dir_path)
print(1)
process_data(my_html)
print(" تموم شد به حق علی")