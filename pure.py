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
}

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
                    if node.get(key) is not None:
                        add_up_compare(d1[key], d2[key], node[key])
        return node

    return add_up_compare(d1, d2, comparison_json)

INDENTATION_UNIT = " " * 4
def generate_html_recursive_v3(data, colors, indent_level=1):
    html_lines = []
    indent = INDENTATION_UNIT * indent_level
    
    for key, value in data.items():
        color = colors.get(key, {})
        if type(color) != str:
            display_color = None
        else:
            display_color = {
                "Yellow": "Yellow",
                "Green": "#00FF00",
                "Red": "#FF0000",
            }[color]
            color = {}
        
        if isinstance(value, dict):
            nested_html = generate_html_recursive_v3(value, color, indent_level + 1)
            line = f'{indent}<span style="background-color: {display_color};">"{key}"</span>: {{\n{nested_html}\n{indent}}}'
        elif isinstance(value, list):
            nested_lines = []
            for item in value:
                if isinstance(item, dict):
                    nested_lines.append(f'{INDENTATION_UNIT}{{\n{generate_html_recursive_v3(item, color, indent_level + 2)}\n{indent}{INDENTATION_UNIT}}}')
                else:
                    nested_lines.append(f'{indent}{item}')
            temp_cal = f",\n{indent}".join(nested_lines)
            nested_content = f'{indent}<span style="background-color: {display_color};">"{key}"</span>: [\n{indent}{temp_cal}\n{indent}]'
            line = nested_content
        else:
            line = f'{indent}<span style="background-color: {display_color};">"{key}": {value}</span>'
        html_lines.append(line)
    
    return ',\n'.join(html_lines)
 
def generate_html(data_json, color_json):
    html_content = generate_html_recursive_v3(data_json, color_json)
    final_html = f'<pre>{{\n{html_content}\n}}</pre>'
    return final_html

if __name__ == '__main__':
    color_json = compare_dict_v4(jA, jB)
    html_output_1 = generate_html(jA, color_json)
    html_output_2 = generate_html(jB, color_json)
    boxed_html_output_1 = f'<div style="width: 50%; border: 1px solid #000; padding: 10px;">{html_output_1}</div>'
    boxed_html_output_2 = f'<div style="width: 50%; border: 1px solid #000; padding: 10px;">{html_output_2}</div>'

    side_by_side_html = f'<div style="display: flex; width: 100%;">\n{boxed_html_output_1}\n{boxed_html_output_2}\n</div>'
    
    # Save the combined HTML content to a file
    with open("pure_output.html", "w") as html_file:
        html_file.write(side_by_side_html)
