import pyquran as quranPkg
from typing import List


class QuranRetrivalInterface:

    async def get_sura_content(self, sura_number: int, with_tashkeel: bool = False, basmalah: bool = False):
        return quranPkg.quran.get_sura(sura_number, with_tashkeel, basmalah)

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
        return quranPkg.buckwalter_transliteration(str(verse), reverse)
