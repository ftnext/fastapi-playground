import json
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


@step("メディアタイプ<media_type>で")
def set_content_type_header(media_type: str):
    data_store.spec.setdefault("kwargs", {})["headers"] = {"Content-Type": media_type}


@step("JSON<json_data>で")
def set_json_data(json_str: str):
    data_store.spec.setdefault("kwargs", {})["json"] = json.loads(json_str)


@step("リクエストを送る")
def send_request():
    endpoint = urljoin(BASE_URL, data_store.spec["path"])
    method = data_store.spec["method"].lower()
    kwargs = data_store.spec.get("kwargs", {})
    response = httpx.request(method, endpoint, **kwargs)
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
