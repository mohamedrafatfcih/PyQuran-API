from pydantic import BaseModel
from typing import List, Union


class Verse(BaseModel):
    number: int = 0
    content: str = ""
    letters: List[str] = None


class SuraConfigs(BaseModel):
    name: str = None
    number: int = None  # Refactor to list
    selected_verse_number: int = None  # Refactor to list & configs
    with_tashkeel: bool = False
    with_basmalh: bool = False
    verse_backwalter_reverse = False
    with_letters: bool = False


class Sura(BaseModel):
    configs: SuraConfigs = None
    verses: Union[List[Verse], Verse] = None
    verses_count: int = 0

    def count_verses(self) -> int:
        self.verses_count = len(
            self.verses) - 1 if self.configs.with_basmalh else len(self.verses)
        return self.verses_count
