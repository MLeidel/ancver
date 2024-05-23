## Web Anchor Verifier

### Ahoy Raspberry Pythonistas

__Problem:__  
I have a webpage with over 50 links to other websites.
How can I periodically verify that each URL still points
to a valid website domain and entry point?

__Solution 1:__  
Click on each link and see what happens.  
_Outcome:_ Works but takes a long time to do.

__Solution 2:__  
Use "Anchor Verifier" a small python program.  
_Outcome:_ Works and is much faster than Solution 1.

__Discussion:__  
Solution 2 could actually be more work than Solution 1 if
you do not have Python3 and its libraries installed on your computer.
Fortunatly, that is described in many places on the Internet.

Here is the program __ancver.py__:  
```python
'''
anchor verify
USE: python3 anchor.py URL print|try|open|
print : report request status to console
try : report status to console and launch error URLs in browser
open : launch all URLs in browser

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

```

This little program is valuable to learn for several reasons. 
First, it will solve our problem discussed above, allowing us to rapidly 
verify each anchor tag that we choose to review. Secondly, this program
demonstrates how to use three very useful Python libraries related to 
Internet access from your desktop.

Some forethought is required in that when you create your anchor tags you will
need to put in one more attribute into each anchor you will want to check with
the anchor verifier program. We'll call this attribute "_scan_". So your anchor tag
will look like this:  
  `<a scan href="someurl.com">text</a>`

The reason for this "scan" attribute is that there could be certain anchor tags you do not want
to verify, and so without the "scan" attribute they will be bypassed.

>
[[ _How could you alter the program to find all anchor tags?_ ]]

__Running the program:__  

ancver.py https://yourwebpage.xyz {print | open}

Here is a portion of the page being tested:  
```html
<body>
<h1>Hello Anchors</h1>
<a scan href="https://google.com">Google</a>
<a scan href="https://faceboo.com">Facebook</a>
<a scan href="https://amazon.com/customerx/">Amazon</a>
<a scan href="https://apple.com">Apple</a>
<a href="my.pdf">My PDF file</a>
<a scan href="https://microsoft.com/news">microsoft</a>
</body>

```

Now we'll run the program and display its output:  
```bash

$> python3 ancver.py https://somesite.com/test print

```
```bash
200
----------
https://google.com
301 Moved Permanently
----------
https://facebooky.com
request failed: invalid URL?, or try URL in browser.
----------
https://amazon.com/frodo/
301 Moved Permanently
----------
https://apple.com
301 Moved Permanently
----------
https://microsoft.com/news
301 Moved Permanently

Found 1 errors.
```
If the request succeeds but returns a number other than 200, then
that error code is displayed with a message (not shown.)
Also, note that the `<a href="my.pdf">My PDF file</a>` anchor was not
tested.

If you run the program with the "open" option, then the "webbrowser" open function
will open each link in a separate tab in your default browser.

The really useful part of Python is its many libraries.
Both BeautifulSoup and requests libraries are powerful tools for many
types of applications. Get to know them well.


