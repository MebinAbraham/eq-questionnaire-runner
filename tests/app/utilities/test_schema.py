import os

import pytest
from app.utilities.schema import (
    get_allowed_languages,
    get_schema_path_map,
    get_schema_name_from_census_params,
    get_schema_path_map_for_language,
)


def test_valid_schema_names_from_census_params():
    assert (
        get_schema_name_from_census_params("census", "I", "GB-WLS")
        == "census_individual_gb_wls"
    )
    assert (
        get_schema_name_from_census_params("census", "H", "GB-WLS")
        == "census_household_gb_wls"
    )
    assert (
        get_schema_name_from_census_params("census", "C", "GB-WLS")
        == "census_communal_establishment_gb_wls"
    )


def test_get_schema_name_from_census_params_invalid_form_type():
    with pytest.raises(ValueError):
        get_schema_name_from_census_params("census", "bad", "GB-WLS")


@pytest.mark.parametrize(
    "schema_name, launch_language, expected",
    [
        ("census_individual_gb_wls", "en", ["en", "cy"]),
        ("census_individual_gb_wls", "cy", ["en", "cy"]),
        ("census_individual_gb_nir", "en", ["en"]),
        ("census_individual_gb_nir", "ga", ["en", "ga"]),
        ("census_individual_gb_nir", "eo", ["en", "eo"]),
        ("invalid_schema_name", "en", ["en"]),
        ("test_language", "invalid_language", ["en"]),
        ("test_language", None, ["en"]),
    ],
)
def test_get_allowed_languages(schema_name, launch_language, expected):
    assert get_allowed_languages(schema_name, launch_language) == expected


def test_get_schema_path_map():
    schema_path_map = get_schema_path_map()

    assert all(
        language_code in schema_path_map.keys() for language_code in ["en", "cy"]
    )
    assert all(os.path.exists(path) for path in schema_path_map["en"].values())


def test_get_schema_path_map_for_language():
    schema_path_map_for_language = get_schema_path_map_for_language("en")

    assert all(os.path.exists(path) for path in schema_path_map_for_language.values())
    assert all(
        os.path.basename(path).replace(".json", "") == schema_name
        for schema_name, path in schema_path_map_for_language.items()
    )
