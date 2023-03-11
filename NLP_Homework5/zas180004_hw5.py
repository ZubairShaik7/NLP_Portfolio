from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from urllib.request import Request, urlopen
import time

# def visible(element):
# if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
#   return False
# elif re.match('<!--.*-->', str(element.encode('utf-8'))):
#    return False
# return True


starter_url = 'https://www.google.com/search?q=luka+doncic&sxsrf=AJOqlzWVkUwG9lesOnoZk6eUIjX2K9KURg%3A1678514417687&ei=8RgMZNPJKamuqtsPhaKZqAs&gs_ssp=eJzj4tbP1TcwNDYtjk-uMmD04s4pzU5USMnPS85MBgBlEQgc&oq=luka+&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMgoILhCxAxBDEOoEMgQIABBDMgcIABCxAxBDMggIABCABBCxAzIICAAQgAQQsQMyCwgAEIAEELEDEIMBMggILhCABBCxAzIICAAQgAQQsQMyBQgAEIAEMgsIABCABBCxAxCDATIVCC4QsQMQQxDqBBDcBBDeBBDgBBgDOgoIABBHENYEELADOgcIABCwAxBDOg0IABDkAhDWBBCwAxgBOgwILhDIAxCwAxBDGAI6BAgjECc6CgguEIMBELEDEEM6BAguEEM6EQguEIAEELEDEIMBEMcBENEDOhEILhCABBCxAxDHARDRAxDUAjoICC4QsQMQgwE6BQguEIAEOggILhCABBDlBDoOCAAQgAQQsQMQgwEQiwNKBAhBGABQgwZYnAtg-BNoA3ABeACAATyIAZoCkgEBNZgBAKABAcgBELgBAsABAdoBBggBEAEYCdoBBggCEAEYCNoBBggDEAEYFA&sclient=gws-wiz-serp'
r = requests.get(starter_url)

data = r.text
soup = BeautifulSoup(data, features="lxml")

# write urls to a file
with open('urls.txt', 'w') as f:
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        print(link_str)
        if 'doncic' in link_str or 'Doncic' in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'google' not in link_str:
                f.write(link_str + '\n')

# end of program
print("end of crawler")

with open('urls.txt', 'r') as f:
    urls = f.read().splitlines()
for u in urls:
    print(u)

file = open('urls.txt', 'r')
URL_files = file.readlines()


# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


for i in URL_files:
    url = i
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    webpage = requests.get(url, headers=headers)
    # html = urllib.request.urlopen(my_url)
    soup = BeautifulSoup(webpage.text, features="lxml")
    data = soup.findAll(text=True)
    result = filter(visible, data)
    temp_list = list(result)  # list from filter
    temp_str = ' '.join(temp_list)

print(temp_str)

# for i in URL_files:#[:-1]:
# my_url = i

# html = urllib.request.urlopen(my_url)
# soup = BeautifulSoup(html)
# data = soup.findAll(text=True)
# result = filter(visible, data)
# temp_list = list(result)      # list from filter
# temp_str = ' '.join(temp_list)
# print(temp_str)

# for i in URL_files:
# url = i

# req = Request(
# url=i,
# headers={'User-Agent': 'Mozilla/5.0'}
# )
#  webpage = urlopen(req)#.read()
#  soup = BeautifulSoup(webpage)
#  data = soup.findAll(text=True)
#  result = filter(visible, data)
# temp_list = list(result)  # list from filter
# temp_str = ' '.join(temp_list)