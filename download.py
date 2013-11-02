import os, os.path, sys, re, urllib.request as req, urllib.parse as urlparse
from bs4 import BeautifulSoup as soup
from pyclip import get_clip

protocol = 'http://'
dry_flag = 'd'
dirname_flag = 'r'
cert_flag = 'c'
no_cert_s = '--no-check-certificate'

def curl(url):
    return req.urlopen(url).read()

def get_matches(url, regexp):
    parser = soup(curl(url))
    filtered = filter( lambda a:a.get('href'), parser.findAll('a'))
    return {anchor['href'] for anchor in filtered if regexp.match(anchor['href'])}
    
def wget_doc(url, href, dry, dir, no_cert):
    if dry:
        print(urlparse.urljoin(os.path.dirname(url) if dir else url,href))
    else:
        wget_args = '%s %s'%(no_cert_s if no_cert else '', urlparse.urljoin(os.path.dirname(url) if dir else url,href))
        wget(wget_args)
        
def wget(wget_args):
    os.system('wget %s'%wget_args)
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        wget(get_clip())
    elif len(sys.argv) == 2 or len(sys.argv) > 4:
        print("Usage: download.py <url> <link match regex>")
    else:
        flags = []
        if len(sys.argv) == 4:
            flags = list(sys.argv[3][1:])
        url = sys.argv[1]
        if not url.startswith(protocol):
            url = protocol + url
        regexp = sys.argv[2]
        for match_anchor in get_matches(url, re.compile(regexp)):
            wget_doc(url, match_anchor, dry_flag in flags, dirname_flag in flags, cert_flag in flags)