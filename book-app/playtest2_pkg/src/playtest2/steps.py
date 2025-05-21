import json
import os
from urllib.parse import urljoin

import httpx
from getgauge.python import Table, data_store, step
from jsonpath_ng.ext import parse
from sqlalchemy import text

from .database import Session
from .gauge_table import ProtoTable

BASE_URL = os.getenv("SUT_BASE_URL")


@step("パス<path>に")
def set_path(path: str):
    data_store.spec["path"] = path


class PlayTest2:
    @step("メソッド<method>で")
    def set_method(self, method: str):
        data_store.spec["method"] = method


    @step("メディアタイプ<media_type>で")
    def set_content_type_header(self, media_type: str):
        data_store.spec.setdefault("kwargs", {})["headers"] = {"Content-Type": media_type}


    @step("JSON<json_data>で")
    def set_json_data(self, json_str: str):
        data_store.spec.setdefault("kwargs", {})["json"] = json.loads(json_str)


    @step("リクエストを送る")
    def send_request(self):
        endpoint = urljoin(BASE_URL, data_store.spec["path"])
        method = data_store.spec["method"].lower()
        kwargs = data_store.spec.get("kwargs", {})
        response = httpx.request(method, endpoint, **kwargs)
        data_store.spec["response"] = response


    @step("レスポンスのステータスコードが")
    def get_status_code(self):
        response = data_store.spec["response"]
        data_store.spec["actual"] = response.status_code


    @step("レスポンスのボディが")
    def get_response_body(self):
        response = data_store.spec["response"]
        data_store.spec["response_body_json"] = response.json()


    @step("JSONのパス<json_path>に対応する値が")
    def get_jsonpath_value(self, json_path: str):
        jsonpath_expr = parse(json_path)
        response_json = data_store.spec["response_body_json"]
        matches = jsonpath_expr.find(response_json)
        data_store.spec["actual"] = matches[0].value


    @step("DB<db_name>にSQL<sql>を実行した結果が")
    def execute_sql(self, db_name: str, sql: str):
        with Session() as session:
            result = session.execute(text(sql))
            records = list(result.mappings())

        headers = {"cells": list(records[0].keys())}
        rows = [{"cells": [str(v) for v in r.values()]} for r in records]
        proto_table = ProtoTable({"headers": headers, "rows": rows})
        data_store.spec["actual"] = Table(proto_table)


    @step("文字列の<expected>である")
    def assert_string_value(self, expected: str):
        actual = data_store.spec["actual"]
        assert actual == expected, f"Expected {expected!r} but got {actual!r}"


    @step("整数値の<expected>である")
    def assert_int_value(self, expected: str):
        actual = data_store.spec["actual"]
        expected = int(expected)
        assert actual == expected, f"Expected {expected!r} but got {actual!r}"


    @step("テーブル<expected>である")
    def assert_table(self, expected: Table):
        actual = data_store.spec["actual"]
        assert actual == expected, f"Expected {expected} but got {actual}"
