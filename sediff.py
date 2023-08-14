import json

jA = {
    "A": {
        "B1": "B1",
        "B2": "B2",
        "B4": {
            "C1": "C1",
            "C2": "C2",
            "C4": {
                "D1": "D1"
            },
        },
        "B5": "B51"
    },
    "AL1": ["l0", "l1", "l2"],
    "AL2": ["l1", "l2"],
    "AL3": ["l01"],
    "AL4": ["l0"],
}

jB = {
    "A": {
        "B1": "B1",
        "B3": "B3",
        "B4": {
            "C1": "C1",
            "C3": "C3",
            "C4": "C4",
            "C5": "C5"
        },
        "B5": "B52"
    },
    "AL1": ["l0", "l1", "l2"],
    "AL2": ["l0", "l2"],
    "AL3": ["l02"],
    "AL4": [],
}


def compare_dict(d1, d2, node, reverse=False):
    seq = 0
    for key in d1:
        node[seq] = {}
        node[seq]["key"] = key
        if key not in d2:
            if reverse:
                node[seq]["color"] = "Green"
            else:
                node[seq]["color"] = "Red"
        else:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                node[seq]["data"] = compare_dict(d1[key], d2[key], {}, reverse)
            elif d1[key] != d2[key]:
                node[seq]["color"] = "Yellow"
        seq += 1
    return node

def compare_dict_v2(d1, d2, node, reverse=False):
    for key in d1:
        node[key] = {}
        if key not in d2:
            if reverse:
                node[key]["color"] = "Green"
            else:
                node[key]["color"] = "Red"
        else:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                node[key]["data"] = compare_dict_v2(d1[key], d2[key], {}, reverse)
            elif d1[key] != d2[key]:
                node[key]["color"] = "Yellow"
        if not node[key]:
            node.pop(key)
    return node

def compare_dict_v3(d1, d2, node, reverse=False):
    for key in d1:
        node[key] = {}
        if key not in d2:
            if reverse:
                node[key] = "Green"
            else:
                node[key] = "Red"
        else:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                node[key] = compare_dict_v3(d1[key], d2[key], {}, reverse)
            elif d1[key] != d2[key]:
                node[key] = "Yellow"
        if not node[key]:
            node.pop(key)
    return node

def compare_dict_v4(d1, d2):
    def compare_dict(d1, d2, node):
        for key in d1:
            node[key] = {}
            if key not in d2:
                node[key] = "Red"
            else:
                if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                    node[key] = compare_dict(d1[key], d2[key], {})
                elif d1[key] != d2[key]:
                    node[key] = "Yellow"
            if not node[key]:
                node.pop(key)
        return node
    comparison_json = compare_dict(d1, d2, {})
    def add_up_compare(d1, d2, node):
        for key in d2:
            if key not in d1:
                node[key] = "Green"
            else:
                if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                    add_up_compare(d1[key], d2[key], node[key])
        return node

    return add_up_compare(d1, d2, comparison_json)
    

if __name__ == '__main__':
    # changes_a2b = compare_dict_v3(jA, jB, {}, False)
    changes_a2b = compare_dict_v4(jA, jB)
    # changes_b2a = compare_dict(jB, jA, {}, True)
    print(json.dumps(changes_a2b, indent=4, sort_keys=True))
