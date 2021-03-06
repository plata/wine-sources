import urllib2
from BeautifulSoup import BeautifulSoup
import re
import json

import gecko
import mono

latest_gecko = gecko.get_latest()
latest_mono = mono.get_latest()

upstream_x86 = {
    'name': 'upstream-linux-x86',
    'description': "Upstream linux x86",
    'packages': []
}

upstream_amd64 = {
    'name': 'upstream-linux-amd64',
    'description': "Upstream linux amd64",
    'packages': []
}

staging_x86 = {
    'name': 'staging-linux-x86',
    'description': "Staging linux x86",
    'packages': []
}

staging_amd64 = {
    'name': 'staging-linux-amd64',
    'description': "Staging linux amd64",
    'packages': []
}

base_url = 'https://lutris.net/files/runners/'

response = urllib2.urlopen(base_url)
html = response.read()
soup = BeautifulSoup(html)

# find table with Wine versions
prefix = "wine-"
section = soup.find('body')
rows = section.findAll('a')[1:-1]
for row in rows:
    href = row['href']
    # only wine packages
    if href.startswith(prefix) and (href.endswith('-x86_64.tar.gz') or href.endswith('-i686.tar.gz')):
        filename = href.replace(prefix, '')
        staging = filename.startswith('staging-')
        amd64 = filename.endswith('64.tar.gz')
        package = {
            'version': re.match(r'(staging-)?(.*)-(x86_64|i686)\.tar\.gz', filename).group(2),
            'url': base_url + href,
            'sha1sum': "",
            'geckoFile': latest_gecko['filename-x86_64'] if amd64 else latest_gecko['filename-x86'],
            'geckoUrl': latest_gecko['url-x86_64'] if amd64 else latest_gecko['url-x86'],
            'geckoMd5': None,
            'monoFile': latest_mono['filename'],
            'monoUrl': latest_mono['url'],
            'monoMd5': None
        }
        # find correct category
        if staging:
            if amd64:
                staging_amd64['packages'].append(package)
            else:
                staging_x86['packages'].append(package)
        else:
            if amd64:
                upstream_amd64['packages'].append(package)
            else:
                upstream_x86['packages'].append(package)

versions = [upstream_x86, upstream_amd64, staging_x86, staging_amd64]

with open('lutris-linux.json', 'w') as outfile:
    json.dump(versions, outfile)
