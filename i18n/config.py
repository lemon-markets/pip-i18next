from dataclasses import dataclass, asdict


@dataclass
class Config:
    locale_path: str = "./locale"
    fallback_lang: str = "en"
    fallback_translation: bool = True

    def dict(self):
        return asdict(self)


config = Config()
