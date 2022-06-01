import pyquran as quranPkg


class QuranRetrivalInterface:

    async def get_sura_content(self, sura_number: int, with_tashkeel: bool = False, basmalah: bool = False):
        return quranPkg.quran.get_sura(sura_number, with_tashkeel, basmalah)

    async def get_verse_content(self, sura_number: int, verse_number: int, with_tashkeel: bool = False):
        return quranPkg.quran.get_verse(sura_number, verse_number, with_tashkeel=with_tashkeel)
