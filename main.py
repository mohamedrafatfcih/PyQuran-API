from typing import List
from fastapi import FastAPI
from pyquran_retrival_controller import QuranRetrievalController
from request_validation import RequestValidation


quranRetrievalController = QuranRetrievalController()
quranAppAPI = FastAPI(
    title=quranRetrievalController.constants.quran_api_title,
    description=quranRetrievalController.constants.quran_api_desc,
    version=quranRetrievalController.constants.quran_api_version,
    license_info=quranRetrievalController.constants.quran_api_licence,
    openapi_tags=quranRetrievalController.constants.endpoints_meta_tags,
)
request_validation = RequestValidation()


@quranAppAPI.get("/", tags=["Quran Retrieval"])
async def root_api():
    return {
        "path": "root api",
        "message": "Welcome from quran api."
    }


@quranAppAPI.get("/basmalla", tags=["Quran Retrieval"])
async def basmalla():
    return {"message": "بسم الله الرحمن الرحيم"}


@quranAppAPI.get("/suras/names/", tags=["Quran Retrieval"])
async def get_sura_name(sura_number: int = request_validation.sura_number_validator_optional):
    return await quranRetrievalController.get_sura_name(sura_number)


@quranAppAPI.get("/suras/number", tags=["Quran Retrieval"])
async def get_sura_number(sura_name: str = request_validation.sura_name_validator):
    return await quranRetrievalController.get_sura_number(sura_name)


@quranAppAPI.get("/suras/", tags=["Quran Retrieval"])
async def get_sura(sura_number: int = request_validation.sura_number_validator,  with_tashkeel: bool = False, basmalah: bool = False):
    return await quranRetrievalController.get_sura_content(sura_number, with_tashkeel, basmalah)


@quranAppAPI.get("/suras/verse", tags=["Quran Retrieval"])
async def get_verse(sura_number: int = request_validation.sura_number_validator, verse_number: int = request_validation.verse_number_validator, with_tashkeel: bool = False):
    return await quranRetrievalController.get_verse_content(sura_number, verse_number, with_tashkeel)


@quranAppAPI.get("/quran/suras/", tags=["Quran Retrieval"])
async def get_all_quran(with_tashkeel: bool = False, basmalah: bool = False):
    return await quranRetrievalController.get_all_suras(with_tashkeel=with_tashkeel, basmalah=basmalah)


@quranAppAPI.post("/quran/suras/", tags=["Quran Retrieval"])
async def get_suras_from_quran(suras_numbers: List[int] = request_validation.suras_numbers_list_validator, with_tashkeel: bool = False, basmalah: bool = False):
    return await quranRetrievalController.get_selected_suras_content(suras_numbers, with_tashkeel, basmalah)


@quranAppAPI.get("/suras/verse/backwalter/", tags=["Quran Retrieval"])
async def get_verse_backwalter(sura_number: int = request_validation.sura_number_validator, verse_number: int = request_validation.verse_number_validator, reverse: bool = False):
    return await quranRetrievalController.get_backwalter_transiltration(sura_number, verse_number, reverse)


@quranAppAPI.get("/suras/verse/letters-with-diacritics/", tags=["Quran Retrieval"])
async def split_into_letters_with_diacritics(sura_number: int = request_validation.sura_number_validator, verse_number: int = request_validation.verse_number_validator, with_tashkeel: bool = False):
    return await quranRetrievalController.split_verse_into_letters_diacritics(sura_number, verse_number, with_tashkeel)


@quranAppAPI.get("/defualt-system/", tags=["In Progress"])
async def get_new_defined_system():
    return quranRetrievalController.check_defined_system()


@quranAppAPI.get("/count-text-rasm", tags=["In Progress"])
async def count_text_rasm(sura_number: int, verse_number: int = 0):
    return quranRetrievalController.count_text_rasm(sura_number, verse_number)
