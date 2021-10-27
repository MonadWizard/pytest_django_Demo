import json
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from companies.models import Company

# (((START)))_____________________common part before and after test case implementation
@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):

    #   setUp name can't be changeable and run "before" every test function it's contain common properties
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    #   setUp name can't be changeable and run "after" every test function it's contain common properties
    def tearDown(self) -> None:
        pass


# (((END)))_____________________common part before and after test case implementation


# <<<START>>>_____________________unittest approse implementation
class TestGetCompanies(BasicCompanyAPITestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    #     run by : pytest -v

    def test_one_company_exists_should_success(self) -> None:
        test_company = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        # print(response.content)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), "Amazon")
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
        # delete test company to test database
        test_company.delete()


#     run by : pytest -v -s


class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    #     run by : pytest -v -s

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="Monad")
        response = self.client.post(self.companies_url, data={"name": "Monad"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]},
        )

    def test_create_company_with_only_name_all_field_should_default(self) -> None:
        response = self.client.post(self.companies_url, data={"name": "Monad"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        # print(response.content)
        self.assertEqual(response_content.get("name"), "Monad")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_should_success(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "Monad", "status": "Layoffs"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        # print(response.content)
        self.assertEqual(response_content.get("name"), "Monad")
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "Monad", "status": "WrongStatus"}
        )
        self.assertEqual(response.status_code, 400)
        response_content = json.loads(response.content)
        print(response.content)
        self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))
        # assertIn works for all type of collections


# <<<END>>>_____________________unittest approse implementation

# >>>START<<<_____________________pytest approse POST implementation
# >>>END<<<_____________________pytest approse implementation


# companies_url = reverse("companies-list")
# pytestmark = pytest.mark.django_db
#
#
# # --------------Test Get Companies--------------
# def test_zero_companies_should_return_empty_list(client) -> None:
#     response = client.get(companies_url)
#     assert response.status_code == 200
#     assert json.loads(response.content) == []
#
#
# def test_one_company_exists_should_succeed(client, amazon) -> None:
#     response = client.get(companies_url)
#     response_content = json.loads(response.content)[0]
#     assert response.status_code == 200
#     assert response_content.get("name") == amazon.name
#     assert response_content.get("status") == "Hiring"
#     assert response_content.get("application_link") == ""
#     assert response_content.get("notes") == ""


# # --------------Test Post Companies--------------


# def test_create_company_without_arguments_should_fail(client) -> None:
#     response = client.post(path=companies_url)
#     assert response.status_code == 400
#     assert json.loads(response.content) == {"name": ["This field is required."]}


# def test_create_existing_company_should_fail(client) -> None:
#     Company.objects.create(name="apple")
#     response = client.post(path=companies_url, data={"name": "apple"})
#     assert response.status_code == 400
#     assert json.loads(response.content) == {
#         "name": ["company with this name already exists."]
#     }


# def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
#     response = client.post(path=companies_url, data={"name": "test company name"})
#     assert response.status_code == 201
#     response_content = response.json()
#     assert response_content.get("name") == "test company name"
#     assert response_content.get("status") == "Hiring"
#     assert response_content.get("application_link") == ""
#     assert response_content.get("notes") == ""


# def test_create_company_with_layoffs_status_should_succeed(client) -> None:
#     response = client.post(
#         path=companies_url,
#         data={"name": "test company name", "status": "Layoffs"},
#     )
#     assert response.status_code == 201
#     response_content = json.loads(response.content)
#     assert response_content.get("status") == "Layoffs"


# def test_create_company_with_wrong_status_should_fail(client) -> None:
#     response = client.post(
#         path=companies_url,
#         data={"name": "test company name", "status": "WrongStatus"},
#     )
#     assert response.status_code == 400
#     assert "WrongStatus" in str(response.content)
#     assert "is not a valid choice" in str(response.content)


# @pytest.mark.xfail
# def test_should_be_ok_if_fails() -> None:
#     assert 1 == 2


# @pytest.mark.skip
# def test_should_be_skipped() -> None:
#     assert 1 == 2


# def raise_covid19_exception() -> None:
#     raise ValueError("CoronaVirus Exception")


# def test_raise_covid19_exception_should_pass() -> None:
#     with pytest.raises(ValueError) as e:
#         raise_covid19_exception()
#     assert "CoronaVirus Exception" == str(e.value)


# import logging

# logger = logging.getLogger("CORONA_LOGS")


# def function_that_logs_something() -> None:
#     try:
#         raise ValueError("CoronaVirus Exception")
#     except ValueError as e:
#         logger.warning(f"I am logging {str(e)}")


# def test_logged_warning_level(caplog) -> None:
#     function_that_logs_something()
#     assert "I am logging CoronaVirus Exception" in caplog.text


# def test_logged_info_level(caplog) -> None:
#     with caplog.at_level(logging.INFO):
#         logger.info("I am logging info level")
#         assert "I am logging info level" in caplog.text


# # --------------Learn about fixtures tests--------------


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
