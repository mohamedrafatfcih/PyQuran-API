# PyQuran version and API feature review

This records the gaps before implementation. The [README](README.md#search-and-analysis-routes)
lists the current routes and their inputs.

## Dependency

The API already pins [PyQuran 1.0.1](https://pypi.org/project/pyquran/1.0.1/), the latest version published on PyPI. Keep this pin for the Python 3.12 deployment. The upstream [release branch head](https://github.com/hci-lab/PyQuran/commit/c7a38901b07e60bbfbcaa7eef7d889c0d312faaf) includes a newer change that removes the unused `audioop` import for Python 3.13 compatibility. That checkout has no `pyproject.toml`, `setup.py`, or `setup.cfg`, so switching to it requires making an installable package first. The GitHub source still uses `numpy.int` in its rasm and matrix code, which is incompatible with the API's NumPy 1.26.4 pin.

## API coverage and priorities

| Priority | Feature | Current coverage and next step |
| --- | --- | --- |
| 1 | Quran retrieval and metadata | The API returns chapters, verses, and chapter names and numbers, with options for diacritics and the basmalah. Correct the verse count and numbering when the basmalah flag is used on surahs 1 and 9. Validate verse numbers against the selected surah. Add chapter verse counts and verse token lookup. |
| 2 | Text search | No route exists. Add Arabic word and phrase search with an optional surah filter, a result limit, and chapter, verse, and word positions in the response. Make diacritic matching explicit. |
| 3 | Frequency analysis | No route exists for word frequency, token counts, or character frequency. Start with word frequency for a selected chapter or the whole Quran, with a limit on the result size. |
| 4 | Rasm and alphabet systems | The experimental routes exist, but the count handler builds a result without returning it. Fix NumPy compatibility and verify the shape and meaning of counts per verse before publishing these routes as supported. |
| 5 | Transliteration and diacritics | Verse-based Buckwalter transliteration and letter grouping are exposed. Add text input for Buckwalter encoding and decoding. The current reverse flag still starts from an Arabic verse rather than a Buckwalter string. Add diacritic pattern search and similarity thresholds after text search works. |

The inventory comes from the [upstream documentation](https://github.com/hci-lab/PyQuran/blob/release/DOCUMENTATION.md), the [library source](https://github.com/hci-lab/PyQuran/blob/release/core/pyquran.py), and the API routes in `main.py`. Local LaTeX and XML export helpers can stay in the Python library. Root extraction and frequency by meaning are described as future work upstream.

This is a source review. The live website and individual routes were not tested.
