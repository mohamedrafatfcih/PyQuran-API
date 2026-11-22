from constants import Constants
from typing import List
from pyquran_interface import QuranRetrievalInterface
from quran_models import SuraConfigs


class QuranRetrievalController:
    constants = Constants()
    quranRetrievalInterface = QuranRetrievalInterface()

    async def get_sura_name(self, sura_number: int):
        sura_configs = SuraConfigs(number=sura_number)
        sura_configs = self.quranRetrievalInterface.get_sura_name(sura_configs)
        return sura_configs.dict(exclude_defaults=True, exclude_unset=True, exclude_none=True)

    async def get_sura_number(self, sura_name: str):
        sura_configs = SuraConfigs(name=sura_name)
        sura_configs = self.quranRetrievalInterface.get_sura_number(
            sura_configs)
        return sura_configs.dict(exclude_defaults=True, exclude_none=True, exclude_unset=True)

    async def get_sura_content(self, sura_number: int, with_tashkeel: bool = False, basmalah: bool = False):
        sura_configs = SuraConfigs(
            number=sura_number, with_tashkeel=with_tashkeel, with_basmalh=basmalah)
        sura = self.quranRetrievalInterface.get_sura_content(
            sura_configs=sura_configs)
        return sura.dict(exclude_none=True, exclude_defaults=True, )

    async def get_verse_content(self, sura_number: int, verse_number: int, with_tashkeel: bool = False):
        sura_configs = SuraConfigs(
            number=sura_number, selected_verse_number=verse_number, with_tashkeel=with_tashkeel)
        verse = self.quranRetrievalInterface.get_verse_content(sura_configs)
        return verse.dict(exclude={"letters"})

    async def get_all_suras(self, with_tashkeel: bool, basmalah: bool):
        sura_configs = SuraConfigs(
            with_tashkeel=with_tashkeel, with_basmalh=basmalah)
        suras = self.quranRetrievalInterface.get_all_suras(sura_configs)
        return suras

    async def get_selected_suras_content(self, suras_numbers: List[int], with_tashkeel: bool, basmalah: bool):
        suras = []
        for sura_number in suras_numbers:
            suras.append(await self.get_sura_content(sura_number, with_tashkeel, basmalah))
        return suras

    async def get_backwalter_transiltration(self, sura_number: int, verse_number: int, reverse: bool):
        sura_configs = SuraConfigs(
            number=sura_number, selected_verse_number=verse_number, verse_backwalter_reverse=reverse)
        verse = self.quranRetrievalInterface.get_backwalter_transiltration(
            sura_configs)
        return verse

    async def split_verse_into_letters_diacritics(self, sura_number: int, verse_number: int, with_tashkeel: bool = False):
        sura_configs = SuraConfigs(
            number=sura_number, selected_verse_number=verse_number, with_tashkeel=with_tashkeel)
        verse = self.quranRetrievalInterface.split_verse_into_letters_diacritics(
            sura_configs)
        return verse
