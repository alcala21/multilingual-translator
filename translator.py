import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.languages = {"en": "french-english", "fr": "english-french"}
        self.names = {"en": "English", "fr": "French"}
        self.msg_1 = 'Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French: '
        self.msg_2 = "Type the word you want to translate: "
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.base_url = "https://context.reverso.net/translation"
        self.lang = None
        self.word = None
        self.code = 0
        self.r = None
        self.translations = None
        self.examples = None

    def start(self):
        self.get_inputs()
        self.request_translation()
        self.parse_html()
        self.print_results()

    @staticmethod
    def extract_content(content_list):
        return [item.text.strip() for item in content_list]

    def get_inputs(self):
        while (lang := input(self.msg_1)) not in ["en", "fr"]:
            continue
        self.lang = lang
        self.word = input(self.msg_2)

    def request_translation(self):
        url = f"{self.base_url}/{self.languages[self.lang]}/{self.word}"
        while self.code != 200:
            self.r = requests.get(url, headers=self.headers)
            self.code = self.r.status_code

    def parse_html(self):
        soup = BeautifulSoup(self.r.content, "html.parser")
        self.translations = self.extract_content(
            soup.find(id="translations-content").find_all(class_="display-term")
        )
        self.examples = self.extract_content(
            soup.find(id="examples-content").find_all(class_="ltr")
        )

    def print_results(self):
        print(f'You chose "{self.lang}" as a language to translate "{self.word}"')
        print(self.code, "OK", end="\n\n")
        print(f"{self.names[self.lang]} Translations:")
        for word in self.translations:
            print(word)
        print()
        print(f"{self.names[self.lang]} Examples:", end="")
        for i, example in enumerate(self.examples):
            if i % 2 == 0:
                print()
            print(example)


if __name__ == "__main__":
    Translator().start()
