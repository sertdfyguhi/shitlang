import requests


class HTTPBuiltins:
    def http_get(self, url: str):
        return requests.get(url).text

    def http_post(self, url: str, data: str, content_type: str = "text/plain"):
        headers = {"Content-Type": content_type}
        return requests.post(url, data=data, headers=headers).text
