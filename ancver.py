'''
anchor verify
USE: python3 anchor.py URL print|try|open|
print : report request status to console
try   : report status to console and launch error URLs in browser
open  : launch all URLs in browser

Anchor tags must be marked with 'scan'. Example:
    <a scan href='https://somedomain.com'>Some Domain</a>
'''

from bs4 import BeautifulSoup
import requests
import webbrowser
import sys
from termcolor import cprint

err = {
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect"
}  # list is incomplete!

errs = 0  # to count errors


if len(sys.argv) != 3:
    print("Missing args: URL print|open")
    sys.exit(1)

r = requests.get(sys.argv[1], timeout=(4,5))  # loads the page with the links to be tested
print(r.status_code)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

anchor_tags = soup.find_all('a', attrs={'scan': True})  # locate anchor tags with "scan" attribute

urls = [tag['href'] for tag in anchor_tags if 'href' in tag.attrs]  # create list of URLs

action = sys.argv[2].lower()  # print, try, or open

# Process the list of URLs
for url in urls:
    if errs > 30:
        print("Too many errors!")
        sys.exit(1)

    if url.startswith("http"):
        if action == "open":
            webbrowser.open(url)
        else:
            print("----------")
            print(url)
            try:
                r = requests.head(url, timeout=(4,11))  # using 'head', faster than 'get'
            except requests.exceptions.Timeout:
                cprint("Request Timed Out, try URL in browser", 'red', attrs=['bold',])
                errs += 1
                if action == "try":
                    webbrowser.open(url)
            except Exception as e:
                cprint("request failed: invalid URL?, or try URL in browser.",
                                                                           'red',
                                                                           attrs=['bold',])
                errs += 1
                if action == "try":
                    webbrowser.open(url)
            else:
                error_msg = err.get(r.status_code, " OK")
                # Many status codes other than 200 will occur
                # because of website security and the fact that
                # our requests are not made from a browser!
                # So these are assumed to be OK and they'll
                # be printed out with the code and message.
                print(r.status_code, error_msg)

print(f"\nFound {errs} errors.")
