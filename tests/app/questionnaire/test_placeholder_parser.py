from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


def test_parse_placeholders(placeholder_list, parser):
    placeholders = parser(placeholder_list)

    assert isinstance(placeholders, dict)
    assert "first_name" in placeholders
    assert placeholders["first_name"] == "Joe"


def test_metadata_placeholder():
    placeholder_list = [
        {
            "placeholder": "period",
            "value": {"source": "metadata", "identifier": "period_str"},
        }
    ]

    period_str = "Aug 2018"
    parser = PlaceholderParser(language="en", metadata={"period_str": period_str})

    placeholders = parser(placeholder_list)
    assert period_str == placeholders["period"]


def test_previous_answer_transform_placeholder():
    placeholder_list = [
        {
            "placeholder": "total_turnover",
            "transforms": [
                {
                    "transform": "format_currency",
                    "arguments": {
                        "number": {
                            "source": "answers",
                            "identifier": "total-retail-turnover-answer",
                        }
                    },
                }
            ],
        }
    ]

    retail_turnover = "1000"

    answer_store = AnswerStore(
        [{"answer_id": "total-retail-turnover-answer", "value": retail_turnover}]
    )

    parser = PlaceholderParser(
        language="en", schema=QuestionnaireSchema({}), answer_store=answer_store
    )
    placeholders = parser(placeholder_list)

    assert placeholders["total_turnover"] == "£1,000.00"


def test_metadata_transform_placeholder():
    placeholder_list = [
        {
            "placeholder": "start_date",
            "transforms": [
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {
                            "source": "metadata",
                            "identifier": "ref_p_start_date",
                        },
                        "date_format": "EEEE d MMMM yyyy",
                    },
                }
            ],
        }
    ]

    parser = PlaceholderParser(
        language="en", metadata={"ref_p_start_date": "2019-02-11"}
    )
    placeholders = parser(placeholder_list)

    assert placeholders["start_date"] == "Monday 11 February 2019"


def test_multiple_answer_transform_placeholder():
    placeholder_list = [
        {
            "placeholder": "persons_name",
            "transforms": [
                {
                    "transform": "concatenate_list",
                    "arguments": {
                        "list_to_concatenate": {
                            "source": "answers",
                            "identifier": ["first-name", "last-name"],
                        },
                        "delimiter": " ",
                    },
                }
            ],
        }
    ]

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [
                {"answer_id": "first-name", "value": "Joe"},
                {"answer_id": "last-name", "value": "Bloggs"},
            ]
        ),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["persons_name"] == "Joe Bloggs"


def test_format_list_answer_transform_placeholder():
    placeholder_list = [
        {
            "placeholder": "toppings",
            "transforms": [
                {
                    "transform": "format_list",
                    "arguments": {
                        "list_to_format": {
                            "source": "answers",
                            "identifier": "checkbox-answer",
                        }
                    },
                }
            ],
        }
    ]

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [{"answer_id": "checkbox-answer", "value": ["Ham", "Cheese"]}]
        ),
    )

    placeholders = parser(placeholder_list)

    assert placeholders["toppings"] == "<ul><li>Ham</li><li>Cheese</li></ul>"


def test_multiple_metadata_transform_placeholder():
    placeholder_list = [
        {
            "placeholder": "start_date",
            "transforms": [
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {
                            "source": "metadata",
                            "identifier": "ref_p_start_date",
                        },
                        "date_format": "yyyy-MM-dd",
                    },
                },
                {
                    "transform": "format_date",
                    "arguments": {
                        "date_to_format": {"source": "previous_transform"},
                        "date_format": "dd/MM/yyyy",
                    },
                },
            ],
        }
    ]

    parser = PlaceholderParser(
        language="en", metadata={"ref_p_start_date": "2019-02-11"}
    )

    placeholders = parser(placeholder_list)

    assert placeholders["start_date"] == "11/02/2019"


def test_multiple_metadata_list_transform_placeholder():
    placeholder_list = [
        {
            "placeholder": "dates",
            "transforms": [
                {
                    "transform": "concatenate_list",
                    "arguments": {
                        "list_to_concatenate": {
                            "source": "metadata",
                            "identifier": ["ref_p_start_date", "ref_p_end_date"],
                        },
                        "delimiter": " ",
                    },
                }
            ],
        }
    ]

    parser = PlaceholderParser(
        language="en",
        metadata={"ref_p_start_date": "2019-02-11", "ref_p_end_date": "2019-10-11"},
    )
    placeholders = parser(placeholder_list)

    assert placeholders["dates"] == "2019-02-11 2019-10-11"


def test_mixed_transform_placeholder():
    placeholder_list = [
        {
            "placeholder": "age",
            "transforms": [
                {
                    "transform": "calculate_date_difference",
                    "arguments": {
                        "first_date": {
                            "source": "answers",
                            "identifier": "date-of-birth-answer",
                        },
                        "second_date": {
                            "source": "metadata",
                            "identifier": "second-date",
                        },
                    },
                }
            ],
        }
    ]

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [{"answer_id": "date-of-birth-answer", "value": "1999-01-01"}]
        ),
        metadata={"second-date": "2019-02-02"},
    )
    placeholders = parser(placeholder_list)

    assert placeholders["age"] == "20 years"


def test_mixed_transform_placeholder_value():
    placeholder_list = [
        {
            "placeholder": "age",
            "transforms": [
                {
                    "transform": "calculate_date_difference",
                    "arguments": {
                        "first_date": {
                            "source": "answers",
                            "identifier": "date-of-birth-answer",
                        },
                        "second_date": {"value": "2019-02-02"},
                    },
                }
            ],
        }
    ]

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [{"answer_id": "date-of-birth-answer", "value": "1999-01-01"}]
        ),
    )
    placeholders = parser(placeholder_list)

    assert placeholders["age"] == "20 years"


def test_list_source_count():
    placeholder_list = [
        {
            "placeholder": "number_of_people",
            "value": {"source": "list", "identifier": "people"},
        }
    ]

    list_store = ListStore()
    list_store.add_list_item("people")
    list_store.add_list_item("people")

    parser = PlaceholderParser(language="en", list_store=list_store)
    placeholders = parser(placeholder_list)

    assert placeholders["number_of_people"] == 2


def test_list_source_count_in_transform():
    placeholder_list = [
        {
            "placeholder": "number_of_people",
            "transforms": [
                {
                    "transform": "add",
                    "arguments": {
                        "lhs": {"source": "list", "identifier": "people"},
                        "rhs": {"value": 1},
                    },
                }
            ],
        }
    ]

    list_store = ListStore()
    list_store.add_list_item("people")

    parser = PlaceholderParser(language="en", list_store=list_store)
    placeholders = parser(placeholder_list)

    assert placeholders["number_of_people"] == 2


def test_chain_transform_placeholder():
    placeholder_list = [
        {
            "placeholder": "persons_name",
            "transforms": [
                {
                    "transform": "concatenate_list",
                    "arguments": {
                        "list_to_concatenate": {
                            "source": "answers",
                            "identifier": ["first-name", "last-name"],
                        },
                        "delimiter": " ",
                    },
                },
                {
                    "transform": "format_possessive",
                    "arguments": {"string_to_format": {"source": "previous_transform"}},
                },
            ],
        }
    ]

    parser = PlaceholderParser(
        language="en",
        answer_store=AnswerStore(
            [
                {"answer_id": "first-name", "value": "Joe"},
                {"answer_id": "last-name", "value": "Bloggs"},
            ]
        ),
    )

    placeholders = parser(placeholder_list)
    assert placeholders["persons_name"] == "Joe Bloggs’"
