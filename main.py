from ctypes import Union
from fastapi import FastAPI
import pyquran as quranPkg
from pyquran_interface import QuranRetrivalInterface

quranAppAPI = FastAPI()
quranRetriavalInterface = QuranRetrivalInterface()


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
    return await quranRetriavalInterface.get_sura_content(sura_number, with_tashkeel, basmalah)


@quranAppAPI.get("/suras/verse")
async def get_verse(sura_number: int, verse_number: int, with_tashkeel: bool = False):
    return await quranRetriavalInterface.get_verse_content(sura_number, verse_number, with_tashkeel)


@quranAppAPI.get("/quran/suras/")
async def get_all_quran():
    suras = []
    for sura_number in range(1, 115):
        sura = await quranRetriavalInterface.get_sura_content(
            sura_number, with_tashkeel=True, basmalah=True)
        suras.append(sura)
    return suras
