# PyQuran-API
FastAPI service for retrieving, searching, and analyzing the Quran's Uthmani
Arabic text using [PyQuran](https://github.com/hci-lab/PyQuran).

- [Live API](https://mrafat.pythonanywhere.com/)
- [Interactive API docs](https://mrafat.pythonanywhere.com/docs)
- [OpenAPI schema](https://mrafat.pythonanywhere.com/openapi.json)

For a quick example, [read the first verse of Al-Fatiha with diacritics](https://mrafat.pythonanywhere.com/suras/verse?sura_number=1&verse_number=1&with_tashkeel=true).

## Run locally

From the API directory, use Python 3.12:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open [the interactive API docs](http://127.0.0.1:8000/docs).

## Search and analysis routes

| Route | Inputs and result |
| --- | --- |
| `GET /suras/verse-count` | `sura_number` returns the canonical verse count. |
| `GET /suras/verse/word` | `sura_number`, `verse_number`, and `word_number` locate a word. Positions start at 1. |
| `GET /search/text` | `q` matches whole words or a phrase within a verse. Set `with_tashkeel=true` for exact diacritic matching. |
| `GET /search/diacritics` | `pattern` is one or more space separated binary words. Each `1` marks a letter with a vowel, tanwin, or shadda. Each `0` marks a letter without those signs, including letters with sukun. Set `threshold` below 1 to allow partial matches of the same length. |
| `GET /analysis/word-frequency` | Counts words without diacritics. |
| `GET /analysis/character-frequency` | Counts non-space characters. Set `with_tashkeel=true` to include diacritics as characters. |
| `GET /analysis/token-count` | Counts whitespace separated words in a surah or one verse. |
| `GET /analysis/alphabet` | Returns the PyQuran alphabet. Set `without_dots=true` to return its letter groups. |
| `GET /count-text-rasm` | Returns letter counts per verse. Set `without_dots=true` to count grouped letters under the first letter of each group. |
| `POST /transliterate/buckwalter` | Send JSON with `text` and optional `reverse`. Reverse decodes Buckwalter text to Arabic. |

Search and frequency routes accept an optional `sura_number` and a result
`limit` from 1 to 200. Search returns the original matched text and its
surah, verse, and starting word numbers. The token and rasm count routes
require `sura_number` and optionally accept `verse_number`.
