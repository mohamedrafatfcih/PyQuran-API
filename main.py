from fastapi import FastAPI
import pyquran as quranPkg

quranAppAPI = FastAPI()


@quranAppAPI.get("/")
async def root_api():
    return {
        "path": "root api",
        "message": "Welcome from quran api."
    }


@quranAppAPI.get("/basmalla")
async def basmalla():
    return {"message": "بسم الله الرحمن الرحيم"}


@quranAppAPI.get("/sura/{sura_number}")
async def get_sura(sura_number: int,  with_tashkeel: bool = False, basmalah: bool = False):
    return quranPkg.quran.get_sura(sura_number, with_tashkeel, basmalah)


@quranAppAPI.get("/sura/{sura_number}/verse/{verse_number}")
async def get_verse(sura_number: int, verse_number: int, with_tashkeel: bool = False):
    return quranPkg.quran.get_verse(sura_number, verse_number, with_tashkeel)
