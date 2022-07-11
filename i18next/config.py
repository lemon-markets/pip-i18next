from dataclasses import dataclass, asdict


@dataclass
class Config:
    locale_path: str = "./locales"
    fallback_lang: str = "en"
    strict: bool = False

    def dict(self):
        return asdict(self)


config = Config()
