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

## Update the PythonAnywhere website

These steps update the existing FastAPI site at
`https://mrafat.pythonanywhere.com`. They assume the first deployment created
the app directory `~/pyquran_api` and the Python 3.12 environment
`~/.virtualenvs/pyquran`.

1. In your local clone of the GitHub repository, update `master` and make a ZIP
   containing the app files:

   ```bash
   git switch master &&
     git pull --ff-only origin master &&
     git archive --format=zip --prefix=pyquran_api/ \
       --output=PyQuran-API-update.zip HEAD -- '*.py' requirements.txt
   ```

2. In the [PythonAnywhere dashboard](https://www.pythonanywhere.com/user/mrafat/),
   open **Files** and upload `PyQuran-API-update.zip` to your home directory.
   If a ZIP from a previous update is already there, replace it with this one.

3. Open **Consoles → Bash** on PythonAnywhere and run:

   ```bash
   (
     set -e
     cd "$HOME"
     unzip -o PyQuran-API-update.zip
     venv="$HOME/.virtualenvs/pyquran"
     "$venv/bin/python" -m pip install --no-cache-dir \
       -r "$HOME/pyquran_api/requirements.txt"
     "$venv/bin/python" -m pip check
     "$venv/bin/pa" website reload --domain mrafat.pythonanywhere.com
   )
   ```

   Unzipping replaces the deployed copies of the files in the archive. If a
   command fails, fix that error before retrying. If `pa` reports an
   authentication error, check **Account → API Token** in PythonAnywhere.

4. Open the [API docs](https://mrafat.pythonanywhere.com/docs) and check that
   [the first verse of Al-Fatiha](https://mrafat.pythonanywhere.com/suras/verse?sura_number=1&verse_number=1)
   returns JSON with `number: 1`. If the site returns an error, check
   `/var/log/mrafat.pythonanywhere.com.error.log` in **Files**.

If the free site expires, renew it in PythonAnywhere. See the
[PythonAnywhere ASGI guide](https://help.pythonanywhere.com/pages/ASGICommandLine/#reloading)
for more on reloading and logs.

## Deploy on Render

Create a **Web Service** from the `master` branch using the **Docker** runtime.
Use the repository root and its [Dockerfile](Dockerfile), leave **Docker Command**
blank, and set **Health Check Path** to `/`. The container starts the API on
port 8000. Open `/docs` on the service URL after deployment.
