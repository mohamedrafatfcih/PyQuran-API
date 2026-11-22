from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, constr
import pyquran as quranPkg
from docs_ui import DOCS_HEAD
from pyquran_retrival_controller import QuranRetrievalController
from request_validation import RequestValidation, SuraNumber


quranRetrievalController = QuranRetrievalController()
app = FastAPI(
    docs_url=None,
    title=quranRetrievalController.constants.quran_api_title,
    description=quranRetrievalController.constants.quran_api_desc,
    version=quranRetrievalController.constants.quran_api_version,
    license_info=quranRetrievalController.constants.quran_api_licence,
    openapi_tags=quranRetrievalController.constants.endpoints_meta_tags,
)
quranAppAPI = app
request_validation = RequestValidation()
retrieval = quranRetrievalController.quranRetrievalInterface


@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
def api_docs(request: Request):
    root_path = request.scope.get("root_path", "").rstrip("/")
    page = get_swagger_ui_html(
        openapi_url=f"{root_path}{app.openapi_url}",
        title="PyQuran API | Documentation",
        swagger_ui_parameters={"docExpansion": "list", "filter": True, "defaultModelsExpandDepth": -1},
    )
    return HTMLResponse(page.body.decode("utf-8").replace("</head>", f"{DOCS_HEAD}</head>", 1))


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
    """Look up a surah by number. Omit sura_number to list all 114 names in Quran order."""
    return await quranRetrievalController.get_sura_name(sura_number)


@quranAppAPI.get("/suras/number", tags=["Quran Retrieval"])
async def get_sura_number(sura_name: str = request_validation.sura_name_validator):
    """Look up the number for an exact Arabic surah name. An unrecognized name is returned without a number."""
    return await quranRetrievalController.get_sura_number(sura_name)


@quranAppAPI.get("/suras/", tags=["Quran Retrieval"])
async def get_sura(sura_number: int = request_validation.sura_number_validator,  with_tashkeel: bool = False, basmalah: bool = False):
    """Read one surah. Request basmalah to include the opening formula where applicable."""
    return await quranRetrievalController.get_sura_content(sura_number, with_tashkeel, basmalah)


@quranAppAPI.get("/suras/verse", tags=["Quran Retrieval"])
async def get_verse(sura_number: int = request_validation.sura_number_validator, verse_number: int = request_validation.verse_number_validator, with_tashkeel: bool = False):
    """Read one verse by its position within a surah. An out-of-range verse returns 404."""
    return await quranRetrievalController.get_verse_content(sura_number, verse_number, with_tashkeel)


@quranAppAPI.get("/quran/suras/", tags=["Quran Retrieval"])
async def get_all_quran(with_tashkeel: bool = False, basmalah: bool = False):
    """Read all 114 surahs in Quran order. Use the single-surah route for smaller responses."""
    return await quranRetrievalController.get_all_suras(with_tashkeel=with_tashkeel, basmalah=basmalah)


@quranAppAPI.post("/quran/suras/", tags=["Quran Retrieval"])
async def get_suras_from_quran(suras_numbers: List[SuraNumber] = request_validation.suras_numbers_list_validator, with_tashkeel: bool = False, basmalah: bool = False):
    """Read selected surahs in request order. Repeat the query parameter, for example suras_numbers=1&suras_numbers=112."""
    return await quranRetrievalController.get_selected_suras_content(suras_numbers, with_tashkeel, basmalah)


@quranAppAPI.get("/suras/verse/backwalter/", tags=["Quran Retrieval"])
async def get_verse_backwalter(sura_number: int = request_validation.sura_number_validator, verse_number: int = request_validation.verse_number_validator, reverse: bool = False):
    """Encode a retrieved verse as Buckwalter. To decode supplied Buckwalter text, use POST /transliterate/buckwalter."""
    return await quranRetrievalController.get_backwalter_transiltration(sura_number, verse_number, reverse)


@quranAppAPI.get("/suras/verse/letters-with-diacritics/", tags=["Quran Retrieval"])
async def split_into_letters_with_diacritics(sura_number: int = request_validation.sura_number_validator, verse_number: int = request_validation.verse_number_validator, with_tashkeel: bool = False):
    """Split one verse into letter groups. Set with_tashkeel=true to retain diacritics in those groups."""
    return await quranRetrievalController.split_verse_into_letters_diacritics(sura_number, verse_number, with_tashkeel)


@app.get("/suras/verse-count", tags=["Quran Retrieval"])
def verse_count(sura_number: SuraNumber):
    """Return the number of verses in a surah, excluding any added basmalah."""
    return {"sura_number": sura_number, "count": len(quranPkg.quran.get_sura(sura_number))}


@app.get("/suras/verse/word", tags=["Quran Retrieval"])
def verse_word(sura_number: SuraNumber, verse_number: int = Query(..., ge=1),
               word_number: int = Query(..., ge=1), with_tashkeel: bool = False):
    """Return one word at a 1-based position within a verse. An out-of-range position returns 404."""
    _, _, words = next(retrieval.get_words(sura_number, verse_number, with_tashkeel))
    if word_number > len(words):
        raise HTTPException(404, "Word number is outside this verse")
    return {"sura_number": sura_number, "verse_number": verse_number,
            "word_number": word_number, "text": words[word_number - 1]}


@app.get("/search/text", tags=["Search"])
def search_text(q: str = Query(..., min_length=1, max_length=256),
                sura_number: Optional[SuraNumber] = None, with_tashkeel: bool = False,
                limit: int = Query(50, ge=1, le=200)):
    """Find consecutive whole words within a verse. Omit sura_number to search the full Quran. Results include the match and its starting word number."""
    return retrieval.search(q, sura_number, limit, with_tashkeel=with_tashkeel)


@app.get("/search/diacritics", tags=["Search"])
def search_diacritics(pattern: str = Query(..., max_length=128, regex=r"^[01]+(?: [01]+)*$"),
                      sura_number: Optional[SuraNumber] = None, threshold: float = Query(1, gt=0, le=1),
                      limit: int = Query(50, ge=1, le=200)):
    """Match binary patterns against words within a verse. Use 1 for a vowel, tanwin, or shadda and 0 otherwise. Separate word patterns with spaces. A threshold of 1 requires an exact match."""
    return retrieval.search(pattern, sura_number, limit, pattern=True, threshold=threshold)


@app.get("/analysis/word-frequency", tags=["Analysis"])
def word_frequency(sura_number: Optional[SuraNumber] = None,
                   limit: int = Query(50, ge=1, le=200)):
    """Rank words by count after removing diacritics. Omit sura_number for a whole-Quran count."""
    return retrieval.frequency(sura_number, None, limit)


@app.get("/analysis/character-frequency", tags=["Analysis"])
def character_frequency(sura_number: Optional[SuraNumber] = None,
                        with_tashkeel: bool = False, limit: int = Query(50, ge=1, le=200)):
    """Rank non-space characters by count. With tashkeel enabled, diacritics count as separate characters."""
    return retrieval.frequency(sura_number, None, limit, characters=True, with_tashkeel=with_tashkeel)


@app.get("/analysis/token-count", tags=["Analysis"])
def token_count(sura_number: SuraNumber, verse_number: Optional[int] = Query(None, ge=1)):
    """Count whitespace-separated words in a surah or one verse. Omit verse_number to count the surah."""
    return {"sura_number": sura_number, "verse_number": verse_number,
            "count": sum(len(words) for _, _, words in retrieval.get_words(sura_number, verse_number))}


@app.get("/defualt-system/", tags=["Analysis"], deprecated=True)
@app.get("/analysis/alphabet", tags=["Analysis"])
def alphabet_system(without_dots: bool = False):
    """List the default Arabic alphabet or the PyQuran letter groups used for dotless rasm counting."""
    return retrieval.get_rasm_system(without_dots)


@app.get("/count-text-rasm", tags=["Analysis"])
def count_text_rasm(sura_number: SuraNumber, verse_number: int = Query(0, ge=0),
                    without_dots: bool = False):
    """Return a letter-count map for each selected verse. Omit verse_number or use 0 for the whole surah. Dotless mode combines each group under its first letter."""
    return retrieval.count_text_rasm(sura_number, verse_number or None, without_dots)


class TransliterationInput(BaseModel):
    text: constr(min_length=1, max_length=4096)
    reverse: bool = False


@app.post("/transliterate/buckwalter", tags=["Quran Retrieval"])
def transliterate(input: TransliterationInput):
    """Convert caller-supplied Arabic to Buckwalter. Set reverse=true to decode Buckwalter back to Arabic."""
    return {"text": quranPkg.buckwalter_transliteration(input.text, input.reverse)}
