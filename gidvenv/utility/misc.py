import requests


def download_file(url, output_file):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    with open(output_file, 'wb') as out_file:
        out_file.write(response.content)
