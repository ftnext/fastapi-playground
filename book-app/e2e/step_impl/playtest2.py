import os
from urllib.parse import urljoin

import httpx
from getgauge.python import data_store, step

BASE_URL = os.getenv("SUT_BASE_URL")


@step("パス<path>に")
def set_path(path: str):
    data_store.spec["path"] = path


@step("メソッド<method>で")
def set_method(method: str):
    data_store.spec["method"] = method


@step("リクエストを送る")
def send_request():
    endpoint = urljoin(BASE_URL, data_store.spec["path"])
    method = data_store.spec["method"].lower()
    response = httpx.request(method, endpoint)
    data_store.spec["response"] = response


@step("レスポンスのステータスコードが")
def get_status_code():
    response = data_store.spec["response"]
    data_store.spec["actual"] = response.status_code


@step("整数値の<expected>である")
def assert_int_value(expected: str):
    actual = data_store.spec["actual"]
    expected = int(expected)
    assert actual == expected, f"Expected {expected!r} but got {actual!r}"
