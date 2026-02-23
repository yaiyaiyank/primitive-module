from pathlib import Path
import datetime
import json
from typing import Literal
import base64

# TODO 保存したいデータの一部が{TYPE: "tuple", VAL: "hoge"}になっていたら衝突するのでなんとかするかも
# default/object_hook 方式だけで tuple を確実に扱うのは難しいのでなんとかするかも
TYPE = "__type__"
VAL = "__value__"


def _default(o):
    # date -> iso8601文字列で保存(datetimeがdateを継承しているのでかならず先にdatetime)
    if isinstance(o, datetime.datetime):
        return {TYPE: "datetime", VAL: o.isoformat()}

    # date -> iso8601文字列で保存(datetimeがdateを継承しているのでかならず後でdate
    if isinstance(o, datetime.date):
        return {TYPE: "date", VAL: o.isoformat()}

    # bytes -> base64文字列で保存
    if isinstance(o, (bytes, bytearray, memoryview)):
        b = bytes(o)
        return {TYPE: "bytes", VAL: base64.b64encode(b).decode("ascii")}

    # tuple -> list で持って type タグを付ける
    if isinstance(o, tuple):
        return {TYPE: "tuple", VAL: list(o)}

    # Path -> 文字列で保存
    if isinstance(o, Path):
        return {TYPE: "path", VAL: str(o)}

    print(f"Warning: Not JSON serializable: {type(o).__name__}")
    return None


def _object_hook(d: dict):
    t = d.get(TYPE)
    if t == "bytes":
        return base64.b64decode(d[VAL].encode("ascii"))
    if t == "tuple":
        return tuple(d[VAL])
    if t == "path":
        return Path(d[VAL])
    if t == "date":
        return datetime.date.fromisoformat(d[VAL])
    if t == "datetime":
        return datetime.datetime.fromisoformat(d[VAL])
    return d


def _valid_json(json_file_path: Path | str, exists_check: bool = False) -> Path:
    if isinstance(json_file_path, str):
        json_file_path = Path(json_file_path)
    if json_file_path.suffix != ".json":
        raise ValueError("jsonファイルのみです。")
    if exists_check and not json_file_path.exists():
        raise FileNotFoundError("jsonファイルがないです。")
    return json_file_path


def write_json(json_file_path: Path | str, obj):
    json_file_path = _valid_json(json_file_path)
    json_file_path.parent.mkdir(parents=True, exist_ok=True)
    with json_file_path.open("w", encoding="utf8") as f:
        json.dump(obj, f, default=_default, ensure_ascii=False, indent=4)


def read_json(json_file_path: Path | str) -> dict[str]:
    json_file_path = _valid_json(json_file_path, exists_check=True)
    with json_file_path.open("r", encoding="utf8") as f:
        return json.load(f, object_hook=_object_hook)


def dumps(obj):
    return json.dumps(obj, default=_default, ensure_ascii=False)


def loads(string: str):
    return json.loads(string, object_hook=_object_hook)
