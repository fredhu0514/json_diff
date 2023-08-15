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
            "C6": {
                "D2": "D2",
            }
        },
        "B5": "B51",
        "BL1": [
            {
                "bl1": "bl10",
                "bl2": {
                    "bl22": "bl220"
                },
                "bl3": [
                    {
                        "cl1": "cl10",
                        "cl2": {
                            "cl21": "cl210"
                        }
                    }
                ]
            },
            {
                "bl1": "bl11",
                "bl2": {
                    "bl22": "bl221"
                },
                "bl3": [
                    {
                        "cl1": "cl01",
                        "cl2": {
                            "cl21": "cl211"
                        }
                    },
                    {
                        "cl1": "cl02",
                        "cl2": {
                            "cl21": "cl212"
                        }
                    }
                ]
            },
            {
                "bl1": "bl11",
                "bl2": {
                    "bl22": "bl221"
                },
                "bl3": [
                    {
                        "cl1": "cl01",
                        "cl2": {
                            "cl21": "cl211"
                        }
                    }
                ]
            }
        ]
    },
    "AL1": ["l0", "l1", "l2"],
    "AL2": ["l1", "l2"],
    "AL3": ["l01"],
    "AL4": ["l0"],
    "AL5": ["l05"],
    "AL6": ["l05", "l08"]
}

jB = {
    "A": {
        "B1": "B1",
        "B3": "B3",
        "B4": {
            "C1": "C1",
            "C3": "C3",
            "C4": "C4",
            "C5": "C5",
            "C6": {
                "D2": "D2",
            },
            "C7": {
                "D3": "D3",
            }
        },
        "B5": "B52",
        "BL1": [
            {
                "bl1": "bl10",
                "bl2": {
                    "bl22": "bl220"
                },
                "bl3": [
                    {
                        "cl1": "cl10",
                        "cl2": {
                            "cl21": "cl210"
                        }
                    }
                ]
            },
            {
                "bl1": "bl11",
                "bl2": {
                    "bl22": "bl221"
                },
                "bl3": [
                    {
                        "cl1": "cl11",
                        "cl2": {
                            "cl21": "cl211"
                        }
                    }
                ]
            }
        ]
    },
    "AL1": ["l0", "l1", "l2"],
    "AL2": ["l0", "l2"],
    "AL3": ["l02"],
    "AL4": [],
    "AL5": ["l05", "l06"],
    "AL6": ["l05"]
}

def is_empty_structure(data):
    if isinstance(data, dict):
        return all(is_empty_structure(value) for value in data.values())
    elif isinstance(data, list):
        return all(is_empty_structure(item) for item in data)
    else:
        return data is None
    
def compare_list(list1, list2):
    # Compare two lists by comparing their elements one by one
    comparison = {}
    for index, (item1, item2) in enumerate(zip(list1, list2)):
        if isinstance(item1, dict) and isinstance(item2, dict):
            dict_result = compare_dict_v4(item1, item2)
            if not is_empty_structure(dict_result):
                comparison[index] = dict_result
        elif item1 != item2:
            comparison[index] = "Yellow"

    
    # Handle the case where one list is longer than the other
    if len(list1) < len(list2):
        for k in range(len(list1), len(list2)):
            comparison[k] = "Lime"
    else:
        for k in range(len(list2), len(list1)):
            comparison[k] = "Red"
    return comparison

def compare_dict_v4(d1, d2):
    def compare_dict(d1, d2, node):
        for key in d1:
            node[key] = {}
            if key not in d2:
                node[key] = "Red"
            else:
                if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                    node[key] = compare_dict(d1[key], d2[key], {})
                elif isinstance(d1[key], list) and isinstance(d2[key], list):
                    node[key] = compare_list(d1[key], d2[key])
                elif d1[key] != d2[key]:
                    node[key] = "Yellow"
            if is_empty_structure(node[key]):
                node.pop(key)
        return node
    comparison_json = compare_dict(d1, d2, {})
    def add_up_compare(d1, d2, node):
        for key in d2:
            if key not in d1:
                node[key] = "Lime"
            else:
                if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                    if node.get(key) is not None:
                        add_up_compare(d1[key], d2[key], node[key])
        return node

    return add_up_compare(d1, d2, comparison_json)

INDENTATION_UNIT = " " * 4

def generate_html_recursive_v3(data, colors, line_number=1, indent_level=1):
    html_lines = {}
    indent = INDENTATION_UNIT * indent_level
    
    for key, value in data.items():
        try:
            if isinstance(colors, dict):
                color = colors.get(key, {})
            else:
                color = colors
        except Exception as e:
            print()
            print()
            print(data)
            print()
            print(colors)
            print()
            print()
            raise e
        
        if color is None or type(color) != str:
            display_color = None
        else:
            display_color = color
            color = {}
        
        if isinstance(value, dict):
            nested_html, line_number = generate_html_recursive_v3(value, color, line_number, indent_level + 1)
            line = f'{indent}<span style="background-color: {display_color};">"{key}"</span>: {{'
            html_lines[line_number] = line
            line_number += 1
            html_lines.update(nested_html)
            html_lines[line_number] = f'{indent}}}'
        elif isinstance(value, list):
            nested_lines = []
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    nested_color = color.get(index, {}) if isinstance(color, dict) else color
                    nested_html, line_number = generate_html_recursive_v3(item, nested_color, line_number, indent_level + 2)
                    nested_lines.append(f'{INDENTATION_UNIT}{{')
                    nested_lines.extend(nested_html.values())
                    nested_lines.append(f'{indent}{INDENTATION_UNIT}}}')
                else:
                    item_color = color if isinstance(color, str) else color.get(index, None)
                    nested_lines.append(f'{indent}<span style="background-color: {item_color};">{item}</span>')
            line = f'{indent}<span style="background-color: {display_color};">"{key}"</span>: ['
            html_lines[line_number] = line
            line_number += 1
            html_lines.update({line_number: line for line_number, line in enumerate(nested_lines, start=line_number)})
            html_lines[line_number] = f'{indent}]'
        else:
            line = f'{indent}<span style="background-color: {display_color};">"{key}": {value}</span>'
            html_lines[line_number] = line
            line_number += 1
    
    return html_lines, line_number

def generate_html(data_json, color_json):
    html_content = generate_html_recursive_v3(data_json, color_json)
    final_html = f'<pre>{{\n{html_content}\n}}</pre>'
    return final_html

if __name__ == '__main__':
    color_json = compare_dict_v4(jA, jB)
    print(color_json)
    html_output_1 = generate_html(jA, color_json)
    html_output_2 = generate_html(jB, color_json)
    boxed_html_output_1 = f'<div style="width: 50%; border: 1px solid #000; padding: 10px;">{html_output_1}</div>'
    boxed_html_output_2 = f'<div style="width: 50%; border: 1px solid #000; padding: 10px;">{html_output_2}</div>'

    side_by_side_html = f'<div style="display: flex; width: 100%;">\n{boxed_html_output_1}\n{boxed_html_output_2}\n</div>'
    
    # Save the combined HTML content to a file
    with open("pure_output.html", "w") as html_file:
        html_file.write(side_by_side_html)
