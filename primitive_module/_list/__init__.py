from typing import Sized


def unique_preserve_order(list_: list):
    """
    リストに最初に現れる順に重複を排除したリストを返す
    ChatGPT曰くdict.fromkeys(seq)より速い
    """
    seen = set()
    return [x for x in list_ if not (x in seen or seen.add(x))]


def grid_split(list_: list, column_count: int) -> list[list]:
    """
    リストをグリッドへ

    ex)
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

    outputed_lists_count = (list_.__len__() - 1) // column_count + 1
    output_lists = [[] for _ in range(outputed_lists_count)]

    count = -1
    for i, youso in enumerate(list_):
        if i % column_count == 0:
            count += 1
        output_lists[count].append(youso)

    return output_lists


def turn_split(list_: list, outputed_lists_count: int) -> list[list]:
    """
    リストを端から振り分け、端に到達したら折り返す

    ex)
    list_ = [obj1, obj2, obj3, obj4, obj5, obj6, obj7]

    ↓ outputed_lists_count = 3

    return: [
        [obj1, obj6, obj7],
        [obj2, obj5],
        [obj3, obj4]
    ]
    """
    if outputed_lists_count <= 0 or type(outputed_lists_count) != int:
        print("分割数は自然数で")
        raise TypeError

    output_lists = [[] for _ in range(outputed_lists_count)]
    count = 0
    count_up = True

    for youso in list_:
        output_lists[count].append(youso)

        if count_up:
            count += 1
        else:
            count -= 1

        # countが0やoutputed_lists_countのときに折り返し
        if count == -1:
            count_up = True
            count += 1
        elif count == outputed_lists_count:
            count_up = False
            count -= 1

    return output_lists


def len_split(
    list_: list[Sized], switch_length: int, over_ok: bool = True
) -> list[list[Sized]]:  # strな事が多いのであって、__len__があればなんでもいい
    """
    入力リストの各要素(Sized)に__len__メソッドを有するlistに対し、
    各要素(list)の全要素(Sized)の長さの合計がswitch_length以下になるように振り分ける
    ただし、1つの要素の長さがswitch_length超過の場合、over_okがFalseでValueError、Trueでその1つの要素を持つリストになる

    ex)
    input_list = ["ddsfsfsd","asa","3","asasasa","asaaas","6"]

    ↓ switch_length = 7

    output_list = [
        ['ddsfsfsd'], ← len: 8 > 7 (単体でswitch_length超えているのでこの要素のみ。is_more_lenger_okがFalseだと、このときにエラー)
        ['asa', '3'], ← len: 3 + 1 <= 7 (↓の'asasasa'を含めるとlen: 11 > 7なのでここまで)
        ['asasasa'], ← len: 7 <= 7
        ['asaaas', '6'] ← len: 6 + 1 <= 7
    ]
    """
    output_lists = []
    output_list = []
    if [youso for youso in list_ if youso.__len__() > 0].__len__() == 0:
        return []

    for lengther_obj in list_:
        # raise for more_lenger
        if lengther_obj.__len__() == 0:
            continue
        if not over_ok and lengther_obj.__len__() > switch_length:
            print("長すぎる要素があります")
            raise ValueError
        # ブラックジャックのように、2つ目以降で最大まで超えなかったら追加
        output_list.append(lengther_obj)
        if get_sum_length(output_list) > switch_length:
            del output_list[-1]
            if output_list:  # 入力されたリストの1番目が空だったらappendしない
                output_lists.append(output_list)
            output_list = [lengther_obj]  # 新しいlistオブジェクト
    else:
        output_lists.append(output_list)

    return output_lists


def get_sum_length(list_: list[Sized]) -> int:
    # __len__がない場合、AttributeError: 'hoge' object has no attribute '__len__'が出るのでわざわざhasattr(obj, '__len__')しなくていい
    lemgth = 0
    for lenger_obj in list_:
        lemgth += lenger_obj.__len__()
    return lemgth
