#     links = soup.find_all('a')#, {'href': re.compile(rf".*{domain}*\/.*")})
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(message)s',
    level=logging.INFO)



visited = []                                            # visited urls
not_visited = []                                        # urls found but still not visited
banned_keywords = []                                    # keywords like logout


def _crawl(url):

    linked=[]
    html=requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        path = link.get('href')
        if path and path.startswith('/'):
            path = urljoin(url, path)
            linked.append(path)
    for u in linked:
        if u not in visited and u not in not_visited:
            not_visited.append(u)
        

def _crawling():

    print('[+] Crawling Started...\n')
    while not_visited:
        url = not_visited.pop(0)
        logging.info(f'Crawling: {url}')
        try:
            _crawl(url)
        except Exception:
            logging.exception(f'Failed to crawl: {url}')
        finally:
            visited.append(url)
            with open('urls.csv', 'a') as file:
                file.write(f"{url}\n")
    print("Crawling Done. Results Saved in [urls.csv].")


if __name__ == '__main__':

    init_url='https://www.imdb.com/'
    not_visited.append(init_url)
    _crawling()
