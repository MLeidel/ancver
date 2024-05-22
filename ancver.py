'''
anchor verify
USE: python3 anchor.py URL print|open

Place a 'scan' attribute in any anchor/href tags that you
may wish to check veracity on later.

example:
    <a scan href='https://somedomain.com'>Some Domain</a>
'''

from bs4 import BeautifulSoup
import requests
import webbrowser
import sys
from termcolor import cprint

if len(sys.argv) != 3:
    print("Missing args: URL print|open")
    sys.exit(1)

r = requests.get(sys.argv[1])  # loads the page with the links to be tested
print(r.status_code)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

anchor_tags = soup.find_all('a', attrs={'scan': True})  # locate anchor tags with "scan" attribute

urls = [tag['href'] for tag in anchor_tags if 'href' in tag.attrs]  # create list of URLs

# Process the list of URLs
for url in urls:
    if url.startswith("http"):
        if sys.argv[2].lower() == "open":
            webbrowser.open(url)
        else:
            print("----------")
            print(url)
            try:
                r = requests.get(url)
                if r.status_code != 200:
                    cprint(r.status_code + " ?", 'red', attrs=['bold',])
                else:
                    print("200 OK")
            except Exception as e:
                cprint("request failed: invalid URL?, or try URL in browser.",
                                                                           'red',
                                                                           attrs=['bold',])
