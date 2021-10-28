import json
import pytest
from django.urls import reverse

from companies.models import Company

companies_url = reverse("companies-list")

# reduse decorator duplication by define pytestmark
# pytestmark = [pytest.mark.django_db, pytest.mark.xfail , @pytest.mark.skip]
pytestmark = pytest.mark.django_db

# --------------Test Get Companies--------------

# pytest-django have predefine ficture called client
# @pytest.mark.django_db
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(path=companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


#     run by : pytest -v


def test_one_company_exists_should_success(client) -> None:
    test_company = Company.objects.create(name="Amazon")
    response = client.get(path=companies_url)
    print(response.content)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == "Amazon"
    assert response_content.get("name") == test_company.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""
    # delete test company to test database
    # test_company.delete()   # pytest-django run by creating virtual database so no need this trangation


#     run by : pytest -v -s

# --------------Test Post Companies--------------


def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


#     run by : pytest -v -s


def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="Monad")
    response = client.post(path=companies_url, data={"name": "Monad"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_all_field_should_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "Monad"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    # print(response.content)
    assert response_content.get("name") == "Monad"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_should_success(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "Monad", "status": "Layoffs"}
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    # print(response.content)
    assert response_content.get("name") == "Monad"
    assert response_content.get("status") == "Layoffs"


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "Monad", "status": "WrongStatus"}
    )
    assert response.status_code == 400
    response_content = json.loads(response.content)
    print(response.content)
    assert "WrongStatus" in str(response.content)
    assert "is not a valid choice" in str(response.content)
    # assertIn works for all type of collections


@pytest.mark.xfail
def test_should_be_ok_if_fails() -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped() -> None:
    assert 1 == 2


#   use --durations=N to see how much time it take for all run by : pytest -v -s --duration=0
# for run specific file with pytest by : pytest companies/tests/test_api_pyTest.py


# _______________raise exception________________________


def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


#  specific test can run by giving name, run by pytest -k function_name


# Log:level [ debug:10, info:20, warning:30, error:40, critical:50]
# view define level to maximum Logs

import logging

logger = logging.getLogger("CORONA_LOGS")


def function_that_logs_something() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


# _______________________caplog fixture __________


def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()
    assert "I am logging CoronaVirus Exception" in caplog.text
    print(caplog.text)


# capture all log with "string" if match any, run by pytest file/path/file.py -k "logged"


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
        assert "I am logging info level" in caplog.text


# we can see duration with sort summery for specific test
# run by : pytest -v -s --durations=0 companies/tests/test_api_unitTest.py -k "logged"

# # --------------Learn about fixtures tests--------------

#
# @pytest.mark.parametrize(
#     "companies",
#     [["Tiktok", "Twitch", "Test Company INC"], ["Facebook", "Instagram"]],
#     ids=["3 T companies", "Zuckerberg's companies"],
#     indirect=True,
# )
# def test_multiple_companies_exists_should_succeed(client, companies) -> None:
#     company_names = set(map(lambda x: x.name, companies))
#     print(company_names)
#     response_companies = client.get(companies_url).json()
#     assert len(company_names) == len(response_companies)
#     response_company_names = set(
#         map(lambda company: company.get("name"), response_companies)
#     )
#     assert company_names == response_company_names
