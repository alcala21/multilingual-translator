import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.languages = {
            0: "All",
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
        self.msg_2 = "Type the number of a language you want to translate to or '0' to translate to all languages: "
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
        self.filename = None
        self.log = []

    def start(self):
        self.get_inputs()
        if len(self.to_) == 1:
            self.translate(self.print_multiple)
        elif len(self.to_) > 1:
            self.translate(self.print_one)
        with open(self.filename, "w") as f:
            f.writelines(self.log)

    def translate(self, printer):
        for to_lang in self.to_:
            self.make_url(self.from_, to_lang)
            self.request_translation()
            self.parse_html()
            printer(to_lang)

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
        while (id_2 := self.get_input(self.msg_2)) is None:
            continue
        if id_2 != 0:
            self.to_ = [self.languages[id_2]]
        else:
            self.to_ = [
                self.languages[ix] for ix in self.languages if ix not in [0, id_1]
            ]
        self.word = input(self.msg_3)
        self.filename = f"{self.word}.txt"

    def make_url(self, from_lang, to_lang):
        self.url = f"{self.base_url}/{from_lang.lower()}-{to_lang.lower()}/{self.word}"

    def request_translation(self):
        code = 0
        while code != 200:
            self.r = requests.get(self.url, headers=self.headers)
            code = self.r.status_code
        self.code = code

    def parse_html(self):
        soup = BeautifulSoup(self.r.content, "html.parser")
        self.translations = self.extract_content(
            soup.find(id="translations-content").find_all(class_="display-term")
        )
        self.examples = self.extract_content(
            soup.find(id="examples-content").find_all(class_="text")
        )

    def print_multiple(self, to_lang):
        self.print(f"{to_lang} Translations:")
        for word in self.translations:
            self.print(word)
        self.print()
        self.print(f"{to_lang} Examples:", end="")
        for i, example in enumerate(self.examples):
            if i % 2 == 0:
                self.print()
            self.print(example)

    def print_one(self, to_lang):
        self.print(f"{to_lang} Translations:")
        self.print(self.translations[0])
        self.print()
        self.print(f"{to_lang} Examples:")
        self.print(self.examples[0])
        self.print(self.examples[1])
        self.print()

    def print(self, msg="", end="\n"):
        self.log.append(msg + end)
        print(msg, end=end)


if __name__ == "__main__":
    tr = Translator()
    tr.start()
