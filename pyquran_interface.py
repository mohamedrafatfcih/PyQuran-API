import pyquran as quranPkg
from constants import Constants
from typing import List


class QuranRetrievalInterface:
    constants = Constants()

    async def get_sura_content(self, sura_number: int, with_tashkeel: bool = False, basmalah: bool = False):
        sura = quranPkg.quran.get_sura(sura_number, with_tashkeel, basmalah)
        sura_name = quranPkg.quran.get_sura_name(sura_number)
        return {
            self.constants.sura_number_KEY: sura_number,
            self.constants.sura_name_KEY: sura_name,
            self.constants.sura_KEY: sura,
        }

    async def get_verse_content(self, sura_number: int, verse_number: int, with_tashkeel: bool = False):
        return quranPkg.quran.get_verse(sura_number, verse_number, with_tashkeel=with_tashkeel)

    async def get_all_suras(self, with_tashkeel: bool, basmalah: bool):
        suras = []
        for sura_number in range(1, 115):
            suras.append(await self.get_sura_content(sura_number, with_tashkeel, basmalah))
        return suras

    async def get_selected_suras_content(self, suras_numbers: List[int], with_tashkeel: bool, basmalah: bool):
        suras = []
        for sura_number in suras_numbers:
            suras.append(await self.get_sura_content(sura_number, with_tashkeel, basmalah))
        return suras

    async def get_backwalter_transiltration(self, sura_number: int, verse_number: int, reverse: bool):
        verse = await self.get_verse_content(sura_number, verse_number)
        backwaltered_verse = quranPkg.buckwalter_transliteration(
            str(verse), reverse)
        return {
            self.constants.verse_KEY: verse,
            self.constants.backwaltered_verse_KEY: backwaltered_verse,
        }

    async def split_verse_into_letters_diacritics(self, sura_number: int, verse_number: int):
        verse = await self.get_verse_content(sura_number, verse_number, with_tashkeel=True)
        letters = quranPkg.grouping_letter_diacritics(verse)
        return {self.constants.verse_KEY: verse,
                self.constants.letters_with_diacritics_KEY: letters,
                }
