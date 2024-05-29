from urllib import parse
import requests
import copy
import sys
    
url =sys.argv[1]
url_parsed = parse.urlsplit(url)
params = parse.parse_qs(url_parsed.query)

error_messages = [
    "you have an error in your sql syntax;",
    "warning: mysql",
    "mysql_fetch_array()",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
]

def build_url(url_parsed,query):
    new_params = parse.urlencode(query, doseq=True)
    url = url_parsed._replace(query=new_params)
    return url.geturl()


def request(url):
    if len(sys.argv) > 2:
        headers = sys.argv[2]
    else: headers = {}
    try:
        request = requests.get(url, headers=headers)
        html = request.text
        return html
    except requests.RequestException as e:
        print("Request failed: {}".format(e))
        return None
        
def is_vulnerable(html, url,param):
    if html:
        for error_message in error_messages:
            if error_message in html.lower():
                print("Vulnerabilidade detectada na URL: {}{}".format(url,param))
                return True
    return False

for param in params.keys():
    query = copy.deepcopy(params)
    for e in "\"'":
        query[param][0] = e
        url = build_url(url_parsed, query)
        html = request(url)
        is_vulnerable(html, url, param)


