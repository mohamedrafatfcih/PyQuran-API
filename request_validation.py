from fastapi import Query
from pydantic import conint


class RequestValidation:
    sura_name_validator = Query(
        default=...,
        title="Sura Name",
        description="The arabic name for sura.")

    sura_number_validator = Query(default=..., title="Sura Number",
                                  description="Sura number is integer value.",
                                  ge=1, le=114)
    sura_number_validator_optional = Query(default=None, title="Sura Number",
                                           description="Sura number is integer value.",
                                           ge=1,
                                           le=114,
                                           )
    verse_number_validator = Query(
        default=..., title="Verse Number", ge=1)

    suras_numbers_list_validator = Query(
        default=..., title="Suras Numbers", description="List of suras numbers that you want to retrieve.")


SuraNumber = conint(ge=1, le=114)
