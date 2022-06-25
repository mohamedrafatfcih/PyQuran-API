import pyquran as quranPkg
from typing import List
from quran_models import Sura, SuraConfigs, Verse


class QuranRetrievalInterface:

    def get_sura_content(self, sura_configs: SuraConfigs) -> Sura:
        verses_str_list = quranPkg.quran.get_sura(
            sura_configs.number, sura_configs.with_tashkeel, sura_configs.with_basmalh)
        verses = [self.mapToVerse(sura_configs, verse_str, verse_number)
                  for verse_number, verse_str in enumerate(verses_str_list)]
        sura_configs = self.get_sura_name(sura_configs)
        sura = Sura(configs=sura_configs, verses=verses)
        sura.count_verses()
        return sura

    def mapToVerse(self, sura_configs: SuraConfigs, verse_str: str, verse_number: int) -> Verse:
        verse_number = verse_number if sura_configs.with_basmalh else (
            verse_number + 1)
        verse = Verse(number=verse_number, content=verse_str)
        if sura_configs.with_letters:
            verse.letters = self.get_verse_letters_diacritics(verse_str)
        return verse

    def get_verse_letters_diacritics(self, verse_content: str) -> List[str]:
        return quranPkg.grouping_letter_diacritics(verse_content)

    def get_sura_name(self, sura_configs: SuraConfigs) -> SuraConfigs:
        sura_configs.name = quranPkg.quran.get_sura_name(sura_configs.number)
        return sura_configs

    def get_verse_content(self, sura_configs: SuraConfigs) -> Verse:
        verse_content = quranPkg.quran.get_verse(
            sura_configs.number, sura_configs.selected_verse_number, sura_configs.with_tashkeel)
        letters_diacritics = self.get_verse_letters_diacritics(verse_content)
        return Verse(number=sura_configs.selected_verse_number, content=verse_content, letters=letters_diacritics)

    def get_all_suras(self, sura_configs: SuraConfigs) -> List[Sura]:
        suras: List[Sura] = []
        for sura_number in range(1, 115):
            sura_configs.number = sura_number
            suras.append(self.get_sura_content(sura_configs))
        return suras

    def get_selected_suras_content(self, suras_configs: List[SuraConfigs]) -> List[Sura]:
        suras: List[Sura] = []
        for sura_config in suras_configs:
            suras.append(self.get_sura_content(sura_config))
        return suras

    def get_backwalter_transiltration(self, sura_configs: SuraConfigs) -> Verse:
        verse = self.get_verse_content(sura_configs)
        backwaltered_verse = quranPkg.buckwalter_transliteration(
            str(verse), sura_configs.verse_backwalter_reverse)
        return Verse(sura_configs.selected_verse_number, backwaltered_verse)

    def split_verse_into_letters_diacritics(self, sura_configs: SuraConfigs) -> Verse:
        verse = self.get_verse_content(sura_configs)
        letters = quranPkg.grouping_letter_diacritics(verse.content)
        verse.letters = letters
        return verse

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
