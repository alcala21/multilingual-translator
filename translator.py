import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.languages = {
            1: "Arabic",
            2: "German",
            3: "English",
            4: "Spanish",
            5: "French",
            6: "Hebrew",
            7: "Japanese",
            8: "Dutch",
            9: "Polish",
            10: "Portuguese",
            11: "Romanian",
            12: "Russian",
            13: "Turkish",
        }
        self.names = {"en": "English", "fr": "French"}
        self.msg_0 = "Hello, welcome to the translator. Translator supports: "
        self.msg_1 = "Type the number of your language: "
        self.msg_2 = "Type the number of language you want to translate to: "
        self.msg_3 = "Type the word you want to translate: "
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.base_url = "https://context.reverso.net/translation"
        self.from_ = None
        self.to_ = None
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

    def get_input(self, msg):
        try:
            while (id := int(input(msg))) not in self.languages:
                continue
            return id
        except ValueError:
            return None

    def get_inputs(self):
        print(self.msg_0)
        for key, val in self.languages.items():
            print(f"{key}. {val}")
        while not (id_1 := self.get_input(self.msg_1)):
            continue
        self.from_ = self.languages[id_1]
        while not (id_2 := self.get_input(self.msg_2)):
            continue
        self.to_ = self.languages[id_2]
        self.word = input(self.msg_3)

    def request_translation(self):
        url = f"{self.base_url}/{self.from_.lower()}-{self.to_.lower()}/{self.word}"
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
        print()
        print(f"{self.to_} Translations:")
        for word in self.translations:
            print(word)
        print()
        print(f"{self.to_} Examples:", end="")
        for i, example in enumerate(self.examples):
            if i % 2 == 0:
                print()
            print(example)


if __name__ == "__main__":
    tr = Translator()
    tr.start()
