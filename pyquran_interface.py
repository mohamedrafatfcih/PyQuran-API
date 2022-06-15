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

    def check_defined_system(self):
        return quranPkg.systems.default

    def count_text_rasm(self, sura_number: int, verse_number: int = 0):
        text_for_rasm_count = ""
        sura = quranPkg.quran.get_sura(sura_number)
        if verse_number != 0:
            verse = quranPkg.quran.get_verse(sura_number, verse_number)
            text_for_rasm_count = verse
        else:
            text_for_rasm_count = sura
        defualt_rasm = self.check_defined_system()
        rasm_count_list = quranPkg.count_rasm(
            text_for_rasm_count, defualt_rasm).tolist()
        letter_frequency_dic = []
        for count in range(0, len(rasm_count_list)):
            letter_frequency_dic.append({
                str(defualt_rasm[count][0]): rasm_count_list[count]

            })
