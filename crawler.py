#     links = soup.find_all('a')#, {'href': re.compile(rf".*{domain}*\/.*")})
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import csv

logging.basicConfig(format="%(message)s", level=logging.INFO)


visited = []                        # visited urls
not_visited = []                    # urls found but still not visited
banned_keyword = "logout"           # keywords like logout


def _crawl(url):

    linked = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        path = link.get("href")
        if path and banned_keyword not in path:  # and path.startswith('/'):
            path = urljoin(url, path)
            linked.append(path)
    for u in linked:
        if u not in visited and u not in not_visited:
            not_visited.append(u)


def _crawling():

    print("[+] Crawling Started...\n")
    while not_visited:
        url = not_visited.pop(0)
        logging.info(f"Crawling: {url}")
        try:
            _crawl(url)
        except Exception:
            logging.exception(f"Failed to crawl: {url}")
        finally:
            visited.append(url)
            with open("urls.csv", "a+") as file:
                file.write(f"{url}\n")
    print("Crawling Done. Results Saved in [urls.csv].")


def _parse_form_tags():

    with open("urls.csv", newline="\n") as csvfile:
        urls = list(csv.reader(csvfile))

    form_data = {"data": []}

    for url in urls:
        html = requests.get(url[0]).text
        soup = BeautifulSoup(html, "html.parser")
        for form in soup.find_all("form"):

            form_dict = {}
            inputs_list = []

            action = form.get("action")
            method = form.get("method")
            inputs = form.find_all("input")

            form_dict["action"] = action
            form_dict["method"] = method
            form_dict["url"] = url

            with open("form-details.csv", "a+") as file:
                file.write(f"{url},{method},{action},")
                for _i in inputs:
                    stripped = str(_i).replace("\n", " ")
                    inputs_list.append(stripped)

                    file.write(f"{stripped},")

                file.write("\n")

            form_dict["inputs"] = inputs_list
            form_data["data"].append(form_dict)

    return form_data


if __name__ == "__main__":

    init_url = "https://google.com/"
    not_visited.append(init_url)
    _crawling()
    forms = _parse_form_tags()
