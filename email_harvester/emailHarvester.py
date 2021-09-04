import requests
import re
from bs4 import BeautifulSoup


def harvest_links(url):
    links = []
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        return links

    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        link = str(link.get('href'))
        if link is None:
            continue
        links.append(link)
    return set(links)


def link_refiner(url):
    links = refiner_links(url)
    links_refined = []
    for i in links:
        if (("contact" in i or "Contact" in i)
            or ("Career" in i or "career" in i)) \
                or ('about' in i or "About" in i) \
                or ('Services' in i or 'services' in i):
            links_refined.append(i)
    return set(links_refined)


def email_harvester(soup):
    mails = []
    for name in soup.find_all('a'):
        if name is not None:
            emailText = name.text
            match = bool(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', emailText))
            if '@' in emailText and match == True:
                emailText = emailText.replace(" ", '').replace('\r', '')
                emailText = emailText.replace('\n', '').replace('\t', '')
                if (len(mails) == 0) or (emailText not in mails):
                    print(emailText)
                    mails.append(emailText)
    return mails


def harvest_emails(url):
    emails = []
    for link in link_refiner(url):
        r = requests.get(link)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        if type(email_harvester(soup)) == list:
            if len(email_harvester(soup)) == 0:
                continue
            for m in email_harvester(soup):
                emails.append(m)
        else:
            emails.append(email_harvester(soup))
    return emails


def refiner_links(url):
    links = []
    for j in harvest_links(url):
        if 'http' not in j and 'www' not in j and 'https' not in j:
            links.append(url + j)
            continue
        else:
            links.append(j)
    return links
