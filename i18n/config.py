from dataclasses import dataclass


@dataclass
class Config:
    locale_path: str = "./locale"
    fallback_lang: str = "en"
    fallback_on_missing_translation: bool = True


config = Config()
