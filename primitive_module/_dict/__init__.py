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
