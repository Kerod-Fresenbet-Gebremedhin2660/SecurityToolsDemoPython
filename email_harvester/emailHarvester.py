import requests
import re
from bs4 import BeautifulSoup


def harvest_links(url):
    links = []
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        if link is None:
            continue
        if 'https' in link.get('href') or 'www' in link.get('href') or 'http' in link.get('href') or '.' in link.get('href'):
            links.append(link.get('href'))

    return links


def link_refiner(url):
    links = harvest_links(url)
    links_refined = []
    for i in links:
        if (("contact" in i or "Contact") or ("Career" in i or "career" in i)) or ('about' in i or "About" in i) or (
                'Services' in i or 'services' in i):
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
        if link.startswith("http") or link.startswith("www"):
            r = requests.get(link)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            emails.append(email_harvester(soup))

        else:
            newurl = url + link
            r = requests.get(newurl)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            emails.append(email_harvester(soup))
    return emails


print(harvest_links("http://aait.edu.et/"))
