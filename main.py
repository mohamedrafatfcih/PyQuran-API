from ctypes import Union
from typing import List
from fastapi import FastAPI
import pyquran as quranPkg
from pyquran_interface import QuranRetrievalInterface

quranAppAPI = FastAPI()
quranRetrievalInterface = QuranRetrievalInterface()


@quranAppAPI.get("/")
async def root_api():
    return {
        "path": "root api",
        "message": "Welcome from quran api."
    }


@quranAppAPI.get("/basmalla")
async def basmalla():
    return {"message": "بسم الله الرحمن الرحيم"}


@quranAppAPI.get("/suras/names/")
async def get_sura_name(sura_number: int = None):
    return quranPkg.quran.get_sura_name(sura_number)


@quranAppAPI.get("/suras/number")
async def get_sura_number(sura_name: str):
    return quranPkg.quran.get_sura_number(sura_name)


@quranAppAPI.get("/suras/")
async def get_sura(sura_number: int,  with_tashkeel: bool = False, basmalah: bool = False):
    return await quranRetrievalInterface.get_sura_content(sura_number, with_tashkeel, basmalah)


@quranAppAPI.get("/suras/verse")
async def get_verse(sura_number: int, verse_number: int, with_tashkeel: bool = False):
    return await quranRetrievalInterface.get_verse_content(sura_number, verse_number, with_tashkeel)


@quranAppAPI.get("/quran/suras/")
async def get_all_quran(with_tashkeel: bool = False, basmalah: bool = False):
    return await quranRetrievalInterface.get_all_suras(with_tashkeel=with_tashkeel, basmalah=basmalah)


@quranAppAPI.post("/quran/suras/")
async def get_suras_from_quran(suras_numbers: List[int], with_tashkeel: bool = False, basmalah: bool = False):
    return await quranRetrievalInterface.get_selected_suras_content(suras_numbers, with_tashkeel, basmalah)


@quranAppAPI.get("/suras/verse/backwalter/")
async def get_verse_backwalter(sura_number: int, verse_number: int, reverse: bool = False):
    return await quranRetrievalInterface.get_backwalter_transiltration(sura_number, verse_number, reverse)


@quranAppAPI.get("/suras/verse/letters-with-diacritics/")
async def split_into_letters_with_diacritics(sura_number: int, verse_number: int):
    return await quranRetrievalInterface.split_verse_into_letters_diacritics(sura_number, verse_number)
