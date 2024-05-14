import requests
from .ankiconnect_config import *


class AnkiException(Exception):
    pass


class AnkiModelExists(Exception):
    pass


def invoke(action, **params):
    response = requests.get(
        f"http://127.0.0.1:{global_port}",
        json={"action": action, "params": params, "version": 6},
    ).json()
    if len(response) != 2:
        raise AnkiException("response has an unexpected number of fields")
    if "error" not in response:
        raise AnkiException("response is missing required error field")
    if "result" not in response:
        raise AnkiException("response is missing required result field")
    if response["error"] is not None:
        if response["error"] == "Model name already exists":
            raise AnkiModelExists()
        else:
            raise AnkiException(response["error"])
    return response["result"]


class Deck:
    @staticmethod
    def create(name):
        invoke("createDeck", deck=name)
        return Deck(name)

    @staticmethod
    def NamesAndIds():
        return [Deck(k, v) for k, v in invoke("deckNamesAndIds").items()]

    def __init__(self, name, did=None):
        self.name = name
        self.did = did

    def __repr__(self):
        return f"(Deck {self.name},{self.did})"

    def delete(self):
        return invoke("deleteDecks", decks=[self.name], cardsToo=True)

    @property
    def Config(self):
        return invoke("getDeckConfig", deck=self.name)

    @Config.setter
    def Config(self, config):
        return invoke("saveDeckConfig", config=config)


class Card:
    def __repr__(self):
        return f"(Card {self.cardId})"

    def __init__(self, cardId):
        self.cardId = cardId

    def forget(self):
        return invoke("forgetCards", cards=[self.cardId])

    def relearn(self):
        return invoke("relearnCards", cards=[self.cardId])

    def answer(self):
        return invoke("answerCards", cards=[self.cardId])

    @property
    def Info(self):
        return invoke("cardsInfo", cards=[self.cardId])[0]

    @staticmethod
    def find(query="deck:current"):
        return [Card(_) for _ in invoke("findCards", query=query)]

    @property
    def Deck(self):
        return Deck(list(invoke("getDecks", cards=[self.cardId]).keys())[0])


class Model:
    @staticmethod
    def create(modelName, inOrderFields: list, css, isCloze, cardTemplates):
        try:
            print(
                invoke(
                    "createModel",
                    modelName=modelName,
                    inOrderFields=inOrderFields,
                    css=css,
                    isCloze=isCloze,
                    cardTemplates=cardTemplates,
                )
            )
        except AnkiException as e:
            if str(e) == "Model name already exists":
                pass
            else:
                raise e
        return Model(modelName)

    def __init__(self, name):
        self.name = name

    def updateStyling(self, css):
        return invoke("updateModelStyling", model={"name": self.name, "css": css})

    def updateTemplates(self, templates):
        return invoke(
            "updateModelTemplates", model={"name": self.name, "templates": templates}
        )


class AnkiConnect:
    @staticmethod
    def version() -> int:
        return invoke("version")

    @staticmethod
    def createDeck(deck):
        return invoke("createDeck", deck=deck)

    @staticmethod
    def findCards(query="deck:current"):
        return Card.find(query)


class Note:
    @staticmethod
    def add(
        deckName,
        modelName,
        fields: dict,
        allowDuplicate: bool,
        tags: list,
        audio: list,
        picture: list,
    ):
        invoke(
            "addNote",
            note={
                "deckName": deckName,
                "modelName": modelName,
                "fields": fields,
                "options": {
                    "allowDuplicate": allowDuplicate,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": "Default",
                        "checkChildren": False,
                        "checkAllModels": False,
                    },
                },
                "tags": tags,
                "audio": audio,
                "picture": picture,
            },
        )


if __name__ == "__main__":
    print(AnkiConnect.version())
    print(AnkiConnect.createDeck("shit2"))
    # print(AnkiConnect.findCards()[0].Info['cardId'])
    # print(Card(1504404537724).Info)
    # print(AnkiConnect.findCards()[0].Deck)
    print(Deck.NamesAndIds())
    deck = Deck.NamesAndIds()[0]
    print(deck)
    Deck.create("test1111")
    # print(deck.Config)
    # deck.Config=deck.Config
    # print(deck.delete())
    # print(AnkiConnect.findCards()[0].Deck.delete())

    model = Model.create(
        "newModelName3111",
        ["expression", "sentence", "audio-text", "image"],
        "Optional CSS with default to builtin css",
        False,
        [{"Name": "My Card 1", "Front": html, "Back": html}],
    )

    model.updateStyling("shitcss")
    model.updateTemplates(
        {
            "My Card 1": {
                "Front": html + "shit",
                "Back": html + "shit",
            }
        }
    )
    Note.add(
        "test1111",
        "newModelName3111",
        {
            "expression": "shit122",
            "sentence": "hahaa",
            "meaning": "meaning",
            "glossary-brief": "ss",
            # "audio-text": Media(
            #     r"C:\dataH\LunaTranslator\cache\tts\1714228732.8068416.mp3"
            # ).audio,
        },
        False,
        [],
        [
            # {
            #     "path": r"C:\dataH\LunaTranslator\cache\tts\1714228732.8068416.mp3",
            #     "filename": str(uuid.uuid4()) + "1714228732.8068416.mp3",
            #     "fields": ["audio-text"],
            # }
        ],
        [
            # {
            #     "path": r"C:\Users\11737\Documents\GitHub\LunaTranslator\LunaTranslator\cache\ocr\1709362617.9424458.png",
            #     "filename": str(uuid.uuid4()) + "1714228732.8068416.png",
            #     "fields": ["image"],
            # }
        ],
    )
