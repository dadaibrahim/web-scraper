import urllib.request
from html.parser import HTMLParser

class CustomHTMLParser(HTMLParser):
    def __init__(self, tag, class_name):
        super().__init__()
        self.target_tag = tag
        self.target_class = class_name
        self.is_target = False
        self.data_list = []

    def handle_starttag(self, tag, attrs):
        if tag == self.target_tag:
            attrs = dict(attrs)
            if 'class' in attrs and self.target_class in attrs['class']:
                self.is_target = True

    def handle_endtag(self, tag):
        if tag == self.target_tag and self.is_target:
            self.is_target = False

    def handle_data(self, data):
        if self.is_target:
            self.data_list.append(data.strip())

def scrape_data(url, tag, class_name):
    try:
        response = urllib.request.urlopen(url)
        html_content = response.read().decode('utf-8')
        parser = CustomHTMLParser(tag, class_name)
        parser.feed(html_content)
        parser.close()
        return parser.data_list
    except Exception as e:
        print(f"Failed to fetch data from {url}. Error: {e}")
        return []

def main():
    url = input("Enter the URL of the website to scrape: ")
    tag = input("Enter the HTML tag to scrape: ")
    class_name = input("Enter the class name of the HTML tag: ")
    data = scrape_data(url, tag, class_name)
    if data:
        print(f"Found {len(data)} items")
        for item in data:
            print(item)
    else:
        print("No data found or unable to scrape the website.")

if __name__ == "__main__":
    main()

