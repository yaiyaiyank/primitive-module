from pathlib import Path
import json


def grid_split(dictionary: dict[str], column_count: int) -> list[dict]:
    """
    dictをグリッドへ

    ex) TODO この例はリストなので、後でリスト版を書く
    input_list = [obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8, obj9]

    ↓ column_count = 4

    output_list = [
        [obj1, obj2, obj3, obj4],
        [obj5, obj6, obj7, obj8],
        [obj9]
    ]
    """
    if column_count <= 0 or type(column_count) != int:
        print("分割数は自然数で")
        raise TypeError

    outputed_lists_count = (dictionary.__len__() - 1) // column_count + 1
    output_lists = [dict() for _ in range(outputed_lists_count)]

    count = -1
    for i, dict_item in enumerate(dictionary.items()):
        key, value = dict_item[0], dict_item[1]
        if i % column_count == 0:
            count += 1
        output_lists[count][key] = value

    return output_lists


def _valid_json(json_file_path: Path | str) -> Path:
    if isinstance(json_file_path, str):
        json_file_path = Path(json_file_path)
    if json_file_path.suffix != ".json":
        raise ValueError("jsonファイルのみです。")
    return json_file_path


def write_json(json_file_path: Path | str, dictionary: dict[str]):
    json_file_path = _valid_json(json_file_path)
    with json_file_path.open("w", encoding="utf8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)


def read_json(json_file_path: Path | str) -> dict[str]:
    json_file_path = _valid_json(json_file_path)
    with json_file_path.open("r", encoding="utf8") as f:
        return json.load(f)
