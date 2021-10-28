import json

# use any of this
from unittest import TestCase

# from django.test import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from companies.models import Company


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):

    #   setUp name can't be changeable and run "before" every test function it's contain common properties
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    #   setUp name can't be changeable and run "after" every test function it's contain common properties
    def tearDown(self) -> None:
        pass


# --------------Test Get Companies--------------


class TestGetCompanies(BasicCompanyAPITestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(path=self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    #     run by : pytest -v

    def test_one_company_exists_should_success(self) -> None:
        test_company = Company.objects.create(name="Amazon")
        response = self.client.get(path=self.companies_url)
        print(response.content)
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

# --------------Test Post Companies--------------


class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    #     run by : pytest -v -s

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="Monad")
        response = self.client.post(path=self.companies_url, data={"name": "Monad"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]},
        )

    def test_create_company_with_only_name_all_field_should_default(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "Monad"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        # print(response.content)
        self.assertEqual(response_content.get("name"), "Monad")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_should_success(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "Monad", "status": "Layoffs"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        # print(response.content)
        self.assertEqual(response_content.get("name"), "Monad")
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "Monad", "status": "WrongStatus"}
        )
        self.assertEqual(response.status_code, 400)
        response_content = json.loads(response.content)
        print(response.content)
        self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))
        # assertIn works for all type of collections

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self) -> None:
        assert 1 == 2

    @pytest.mark.skip
    def test_should_be_skipped(self) -> None:
        assert 1 == 2
