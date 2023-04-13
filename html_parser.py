from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data: str) -> None:
        self.result.append(data)

    def handle_entityref(self, name):
        self.result.append('&{};'.format(name))

    def handle_charref(self, name):
        self.result.append('&#{};'.format(name))

    def get_data(self):
        return ''.join(self.result)
