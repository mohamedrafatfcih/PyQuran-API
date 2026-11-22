from collections import Counter
from unicodedata import category, normalize
from pyarabic import araby
import pyquran as quranPkg
from fastapi import HTTPException
from typing import List
from quran_models import Sura, SuraConfigs, Verse


class QuranRetrievalInterface:

    def get_sura_content(self, sura_configs: SuraConfigs) -> Sura:
        verses_str_list = quranPkg.quran.get_sura(
            sura_configs.number, sura_configs.with_tashkeel, sura_configs.with_basmalh)
        first_number = 0 if sura_configs.with_basmalh and sura_configs.number not in (1, 9) else 1
        verses = [self.mapToVerse(sura_configs, verse_str, verse_number)
                  for verse_number, verse_str in enumerate(verses_str_list, first_number)]
        sura_configs = self.get_sura_name(sura_configs)
        sura = Sura(configs=sura_configs, verses=verses)
        sura.count_verses()
        return sura

    def mapToVerse(self, sura_configs: SuraConfigs, verse_str: str, verse_number: int) -> Verse:
        verse = Verse(number=verse_number, content=verse_str)
        if sura_configs.with_letters:
            verse.letters = self.get_verse_letters_diacritics(verse_str)
        return verse

    def get_verse_letters_diacritics(self, verse_content: str) -> List[str]:
        return quranPkg.grouping_letter_diacritics(verse_content)

    def get_sura_name(self, sura_configs: SuraConfigs) -> SuraConfigs:
        sura_configs.name = quranPkg.quran.get_sura_name(sura_configs.number)
        return sura_configs

    def get_sura_number(self, sura_configs: SuraConfigs) -> SuraConfigs:
        sura_configs.number = quranPkg.quran.get_sura_number(sura_configs.name)
        return sura_configs

    def get_verse_content(self, sura_configs: SuraConfigs) -> Verse:
        verse_content = self.get_verse_text(
            sura_configs.number, sura_configs.selected_verse_number, sura_configs.with_tashkeel)
        letters_diacritics = self.get_verse_letters_diacritics(verse_content)
        return Verse(number=sura_configs.selected_verse_number, content=verse_content, letters=letters_diacritics)

    def get_verse_text(self, sura_number: int, verse_number: int, with_tashkeel: bool = False) -> str:
        verses = quranPkg.quran.get_sura(sura_number, with_tashkeel)
        if not 1 <= verse_number <= len(verses):
            raise HTTPException(404, "Verse number is outside this surah")
        return verses[verse_number - 1]

    def get_all_suras(self, sura_configs: SuraConfigs) -> List[Sura]:
        suras: List[Sura] = []
        for sura_number in range(1, 115):
            suras.append(self.get_sura_content(sura_configs.copy(update={"number": sura_number})))
        return suras

    def get_selected_suras_content(self, suras_configs: List[SuraConfigs]) -> List[Sura]:
        suras: List[Sura] = []
        for sura_config in suras_configs:
            suras.append(self.get_sura_content(sura_config))
        return suras

    def get_backwalter_transiltration(self, sura_configs: SuraConfigs) -> Verse:
        verse = self.get_verse_content(sura_configs)
        backwaltered_verse = quranPkg.buckwalter_transliteration(
            verse.content, sura_configs.verse_backwalter_reverse)
        verse.number = sura_configs.selected_verse_number
        verse.content = backwaltered_verse
        return verse

    def split_verse_into_letters_diacritics(self, sura_configs: SuraConfigs) -> Verse:
        verse = self.get_verse_content(sura_configs)
        letters = quranPkg.grouping_letter_diacritics(verse.content)
        verse.letters = letters
        return verse

    def get_words(self, sura_number=None, verse_number=None, with_tashkeel=False):
        if verse_number is not None:
            yield sura_number, verse_number, self.get_verse_text(
                sura_number, verse_number, with_tashkeel
            ).split()
            return
        chapters = range(1, 115) if sura_number is None else (sura_number,)
        for chapter in chapters:
            for number, verse in enumerate(quranPkg.quran.get_sura(chapter, with_tashkeel), 1):
                yield chapter, number, verse.split()

    def search(self, query, sura_number, limit, with_tashkeel=False, pattern=False, threshold=1.0):
        query = normalize("NFC", query)
        if not pattern and not with_tashkeel:
            query = araby.strip_tashkeel(query)
        terms = query.split()
        if not terms:
            raise HTTPException(422, "Search must contain at least one word")
        matches = []
        for chapter, verse, words in self.get_words(sura_number, with_tashkeel=True):
            candidates = [normalize("NFC", word) for word in words]
            if pattern:
                candidates = [diacritic_pattern(word) for word in candidates]
            elif not with_tashkeel:
                candidates = [araby.strip_tashkeel(word) for word in candidates]
            for start in range(len(words) - len(terms) + 1):
                window = candidates[start:start + len(terms)]
                if pattern:
                    if any(len(a) != len(b) for a, b in zip(terms, window)):
                        continue
                    score = sum(
                        expected == actual
                        for a, b in zip(terms, window)
                        for expected, actual in zip(a, b)
                    ) / sum(map(len, terms))
                    if score < threshold:
                        continue
                elif window != terms:
                    continue
                match = {
                    "sura_number": chapter, "verse_number": verse,
                    "word_number": start + 1, "text": " ".join(words[start:start + len(terms)]),
                }
                if pattern:
                    match["similarity"] = score
                matches.append(match)
                if len(matches) == limit:
                    return matches
        return matches

    def frequency(self, sura_number, verse_number, limit, characters=False, with_tashkeel=False):
        counts = Counter()
        for _, _, words in self.get_words(sura_number, verse_number, with_tashkeel):
            counts.update("".join(words) if characters else words)
        key = "character" if characters else "word"
        return [{key: item, "count": count} for item, count in counts.most_common(limit)]

    def get_rasm_system(self, without_dots=False):
        if without_dots:
            return quranPkg.arabic.systems.withoutDots
        return quranPkg.arabic.alphabet

    def count_text_rasm(self, sura_number, verse_number=None, without_dots=False):
        representatives = {letter: letter for letter in self.get_rasm_system()}
        if without_dots:
            for group in self.get_rasm_system(without_dots=True):
                representatives.update(dict.fromkeys(group, group[0]))
        results = []
        for _, number, words in self.get_words(sura_number, verse_number):
            counts = Counter(representatives[char] for word in words for char in word if char in representatives)
            results.append({"verse_number": number, "counts": dict(counts)})
        return results


def diacritic_pattern(word):
    pattern = []
    for char in word:
        if category(char).startswith("M"):
            if pattern and char in araby.TASHKEEL and char != araby.SUKUN:
                pattern[-1] = "1"
        elif char != araby.TATWEEL:
            pattern.append("0")
    return "".join(pattern)
