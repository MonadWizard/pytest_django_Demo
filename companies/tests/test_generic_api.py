# import pytest
# import requests
# import json
#
# testing_env_companies_url = "http://127.0.0.1:8000/companies/"
#
#
# @pytest.mark.skip_in_ci
# @pytest.mark.skip(reason="This test needs localhost django server running")
# def test_zero_companies_django_agnostic() -> None:
#     response = requests.get(url=testing_env_companies_url)
#     assert response.status_code == 200
#     assert json.loads(response.content) == []
#
#
# @pytest.mark.skip_in_ci
# @pytest.mark.skip(reason="This test needs localhost django server running")
# def test_create_company_with_layoffs_django_agnostic() -> None:
#     response = requests.post(
#         url=testing_env_companies_url,
#         json={"name": "test company name", "status": "Layoffs"},
#     )
#     assert response.status_code == 201
#     response_content = json.loads(response.content)
#     assert response_content.get("status") == "Layoffs"
#
#     cleanup_company(company_id=response_content["id"])
#
#
# def cleanup_company(company_id: str) -> None:
#     response = requests.delete(url=f"http://127.0.0.1:8000/companies/{company_id}")
#     assert response.status_code == 204
#
#
# @pytest.mark.crypto
# def test_dogecoin_api() -> None:
#     response = requests.get(
#         url="https://api.cryptonator.com/api/ticker/doge-usd",
#         headers={"User-Agent": "Mozilla/5.0"},
#     )
#
#     assert response.status_code == 200
#     response_content = json.loads(response.content)
#     assert response_content["ticker"]["base"] == "DOGE"
#     assert response_content["ticker"]["target"] == "USD"
#
#
# import responses
#
#
# @pytest.mark.crypto
# @responses.activate
# def test_mocked_dogecoin_api() -> None:
#     responses.add(
#         method=responses.GET,
#         url="https://api.cryptonator.com/api/ticker/doge-usd",
#         json={
#             "ticker": {
#                 "base": "EDEN",
#                 "target": "EDEN-USD",
#                 "price": "0.04535907",
#                 "volume": "4975940509.75870037",
#                 "change": "-0.00052372",
#             },
#             "timestamp": 1612515303,
#             "success": True,
#             "error": "",
#         },
#         status=200,
#     )
#
#     assert process_crypto() == 29
#
#
# def process_crypto() -> int:
#     response = requests.get(
#         url="https://api.cryptonator.com/api/ticker/doge-usd",
#         headers={"User-Agent": "Mozilla/5.0"},
#     )
#
#     response_content = json.loads(response.content)
#     if response.status_code != 200:
#         raise ValueError("Request to Crypto API FAILED!")
#
#     coin_name = response_content["ticker"]["base"]
#     if coin_name == "EDEN":
#         # YAY! We The Response was mocked
#         return 29
#
#     return 42
