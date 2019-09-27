class UrlParser:

    def __init__(self, base_url):
        self.base_url = base_url

    def full(self, relative_url):
        if relative_url[0] == '/':
            relative_url = relative_url[1:]

        return self.base_url + '/' + relative_url

    def relative_and_full(self, relative_url):
        if relative_url[0] == '/':
            relative_url = relative_url[1:]

        return relative_url, self.base_url + '/' + relative_url
