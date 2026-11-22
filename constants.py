class Constants:
    quran_api_title = "PyQuran API"
    quran_api_desc = """Retrieve, search, and analyze the Quran's Uthmani Arabic text using [PyQuran](https://github.com/hci-lab/PyQuran). Responses are JSON.

### Try an example

- [Read the first verse of Al-Fatiha with diacritics](/suras/verse?sura_number=1&verse_number=1&with_tashkeel=true)
- [Find بسم in Al-Fatiha](/search/text?q=%D8%A8%D8%B3%D9%85&sura_number=1)
- [Show the five most frequent words in Al-Fatiha](/analysis/word-frequency?sura_number=1&limit=5)

Expand an operation below and choose **Try it out** to edit its parameters and run it here.

### Numbering and text options

Surah numbers range from 1 to 114. Verse and word positions start at 1. When a surah response includes an added basmalah, that entry is numbered 0 and excluded from the verse count. Al-Fatiha and At-Tawbah receive no added entry.

Where offered, `with_tashkeel=true` preserves Arabic diacritics or asks for exact diacritic matching in text search. For Buckwalter decoding, use `POST /transliterate/buckwalter` with a body such as `{"text":"bsm","reverse":true}`.
"""
    quran_api_version = "0.0.1"
    quran_api_licence = {
        "name": "GNU General Public License v2.0",
        "url": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html"
    }
    endpoints_meta_tags = [
        {
            "name": "Quran Retrieval",
            "description": "Read surahs, verses, and individual words, or convert Arabic text with Buckwalter."
        },
        {
            "name": "Search",
            "description": "Find words, phrases, and diacritic patterns."
        },
        {
            "name": "Analysis",
            "description": "Count Quran words, characters, and letter forms."
        }
    ]

    sura_name_KEY = "sura_name"
    sura_number_KEY = "sura_number"
    sura_KEY = "sura"
    verse_KEY = "verse"
    backwaltered_verse_KEY = "backwaltered_verse"
    letters_with_diacritics_KEY = "letters_with_diacritics"
