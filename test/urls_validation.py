import validators
import requests


def verify_url(urls, timeout=5):
    if isinstance(urls, str):
        urls = [urls]

    sucess = []
    sucess_but = []
    fails = []
    invalid = []

    for url in urls:
        if not validators.url(url):
            invalid.append(url)
            continue

        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                sucess.append(url)
            else:
                sucess_but.append(url)
        except requests.exceptions.Timeout:
            fails.append(f'URL {url} cannot be reached -> Timeout')
        except requests.exceptions.RequestException as e:
            fails.append(f'The URL "{url}" cannot be reached -> ERROR: {e}')

    return {
        "sucess": sucess,
        "sucess_but": sucess_but,
        "fails": fails,
        "invalid": invalid
    }


multiple_urls = ["https://www.google.com.br", "https://www.google.com", "https://url-invalida", "https://exemplo.com"]
multiple_results = verify_url(multiple_urls)


for typ, urls in multiple_results.items():
    if urls:
        print(f"\n{typ.capitalize()}:")
        for url in urls:
            print(url)
