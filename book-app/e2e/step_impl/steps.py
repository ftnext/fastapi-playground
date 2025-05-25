import os
from getgauge.python import Table, data_store, step
from sqlalchemy import text

from .database import Session
from .gauge_table import ProtoTable


@step("DB<db_name>にSQL<sql>を実行した結果が")
def execute_sql(db_name: str, sql: str):
    with Session() as session:
        result = session.execute(text(sql))
        records = list(result.mappings())

    headers = {"cells": list(records[0].keys())}
    rows = [{"cells": [str(v) for v in r.values()]} for r in records]
    proto_table = ProtoTable({"headers": headers, "rows": rows})
    data_store.spec["actual"] = Table(proto_table)


@step("テーブル<expected>である")
def assert_table(expected: Table):
    actual = data_store.spec["actual"]
    assert actual == expected, f"Expected {expected} but got {actual}"
