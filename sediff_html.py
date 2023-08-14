# def generate_html_recursive(data, colors, path, cur_color=None, indent_level=0):
#     html_lines = []
#     indent = " " * 4 * indent_level
    
#     for key, value in data.items():
#         cur_path = path + [key]
#         if cur_color:
#             color = cur_color
#         else:
#             color = dic_recur_get(colors, cur_path)

        
#         if isinstance(value, dict):
#             nested_html = generate_html_recursive(value, colors, cur_path, color, indent_level + 1)
#             line = f'{indent}<span style="color: {color};">"{key}"</span>: {{\n{nested_html}\n{indent}}}'
#         else:
#             line = f'{indent}<span style="color: {color};">"{key}"</span>: {value}'
#         html_lines.append(line)
    
#     return ',\n'.join(html_lines)

# def dic_recur_get(dic, key):

#     temp_dic = dic
#     for k in key:
#         temp_dic = temp_dic.get(k, None)
#         if temp_dic is None:
#             return None
#     if isinstance(temp_dic, dict):
#         return None
#     else:
#         return temp_dic
    
# def generate_html_recursive_v2(data, colors, indent_level=0):
#     html_lines = []
#     indent = " " * 4 * indent_level
    
#     for key, value in data.items():
#         color = colors.get(key, {})
#         if type(color) != str:
#             display_color = None
#         else:
#             display_color = {
#                 "Yellow": "#FFC300",
#                 "Green": "Green",
#                 "Red": "#C41E3A",
#             }[color]
#             color = {}
        
#         if isinstance(value, dict):
#             nested_html = generate_html_recursive_v2(value, color, indent_level + 1)
#             line = f'{indent}<span style="color: {display_color};">"{key}"</span>: {{\n{nested_html}\n{indent}}}'
#         else:
#             line = f'{indent}<span style="color: {display_color};">"{key}": {value}</span>'
#         html_lines.append(line)
    
#     return ',\n'.join(html_lines)

# def generate_html_recursive_v3(data, colors, indent_level=0):
#     html_lines = []
#     indent = " " * 4 * indent_level
    
#     for key, value in data.items():
#         color = colors.get(key, {})
#         if type(color) != str:
#             display_color = None
#         else:
#             display_color = {
#                 "Yellow": "Yellow",
#                 "Green": "#00FF00",
#                 "Red": "#FF0000",
#             }[color]
#             color = {}
        
#         if isinstance(value, dict):
#             nested_html = generate_html_recursive_v3(value, color, indent_level + 1)
#             line = f'{indent}<span style="background-color: {display_color};">"{key}"</span>: {{\n{nested_html}\n{indent}}}'
#         else:
#             line = f'{indent}<span style="background-color: {display_color};">"{key}": {value}</span>'
#         html_lines.append(line)
    
#     return ',\n'.join(html_lines)

INDENTATION_UNIT = " " * 4

# def generate_html_recursive_v3(data, colors, indent_level=1):
#     html_lines = []
#     indent = INDENTATION_UNIT * indent_level
    
#     for key, value in data.items():
#         color = colors.get(key, {})
#         if type(color) != str:
#             display_color = None
#         else:
#             display_color = {
#                 "Yellow": "Yellow",
#                 "Green": "#00FF00",
#                 "Red": "#FF0000",
#             }[color]
#             color = {}
        
#         if isinstance(value, dict):
#             nested_html = generate_html_recursive_v3(value, color, indent_level + 1)
#             line = f'{indent}<span style="background-color: {display_color};">"{key}"</span>: {{\n{nested_html}\n{indent}}}'
#         else:
#             line = f'{indent}<span style="background-color: {display_color};">"{key}": {value}</span>'
#         html_lines.append(line)
    
#     return ',\n'.join(html_lines)

def generate_html_recursive_v4(data1, colors1, data2, colors2, indent_level=1):
    html_lines = []
    indent = INDENTATION_UNIT * indent_level
    
    keys1 = set(data1.keys())
    keys2 = set(data2.keys())
    common_keys = keys1.intersection(keys2)
    
    for key in common_keys:
        value1 = data1[key]
        value2 = data2[key]
        
        color1 = colors1.get(key, {})
        color2 = colors2.get(key, {})
        
        if type(color1) != str:
            display_color1 = None
        else:
            display_color1 = {
                "Yellow": "Yellow",
                "Green": "#00FF00",
                "Red": "#FF0000",
            }[color1]
            color1 = {}
        
        if type(color2) != str:
            display_color2 = None
        else:
            display_color2 = {
                "Yellow": "Yellow",
                "Green": "#00FF00",
                "Red": "#FF0000",
            }[color2]
            color2 = {}
        
        if isinstance(value1, dict) and isinstance(value2, dict):
            nested_html = generate_html_recursive_v4(value1, color1, value2, color2, indent_level + 1)
            nested_formatted = f'\n{nested_html}\n{indent}'
            line = f'{indent}<span style="background-color: {display_color1};">"{key}"</span>: {{\n{nested_formatted}}}'
        else:
            line = f'{indent}<span style="background-color: {display_color1};">"{key}": {value1}</span>'
        html_lines.append(line)
    
    unique_keys1 = keys1 - common_keys
    for key in unique_keys1:
        value1 = data1[key]
        
        color1 = colors1.get(key, {})
        
        if type(color1) != str:
            display_color1 = None
        else:
            display_color1 = {
                "Yellow": "Yellow",
                "Green": "#00FF00",
                "Red": "#FF0000",
            }[color1]
            color1 = {}
        
        if isinstance(value1, dict):
            nested_html = generate_html_recursive_v4(value1, color1, {}, {}, indent_level + 1)
            nested_formatted = f'\n{nested_html}\n{indent}'
            line = f'{indent}<span style="background-color: {display_color1};">"{key}"</span>: {{\n{nested_formatted}}}'
        else:
            line = f'{indent}<span style="background-color: {display_color1};">"{key}": {value1}</span>'
        html_lines.append(line)
    
    unique_keys2 = keys2 - common_keys
    for key in unique_keys2:
        value2 = data2[key]
        
        color2 = colors2.get(key, {})
        
        if type(color2) != str:
            display_color2 = None
        else:
            display_color2 = {
                "Yellow": "Yellow",
                "Green": "#00FF00",
                "Red": "#FF0000",
            }[color2]
            color2 = {}
        
        if isinstance(value2, dict):
            nested_html = generate_html_recursive_v4({}, {}, value2, color2, indent_level + 1)
            nested_formatted = f'\n{nested_html}\n{indent}'
            line = f'{indent}<span style="background-color: {display_color2};">"{key}"</span>: {{\n{nested_formatted}}}'
        else:
            line = f'{indent}<span style="background-color: {display_color2};">"{key}": {value2}</span>'
        html_lines.append(line)
    
    return ',\n'.join(html_lines)

# def generate_html(data_json, color_json):
#     # html_content = generate_html_recursive(data_json, color_json, [])
#     # html_content = generate_html_recursive_v2(data_json, color_json)
#     html_content = generate_html_recursive_v3(data_json, color_json)
#     final_html = f'<pre>{{\n{html_content}\n}}</pre>'
#     return final_html

def generate_html(d1, d2, color_json):
    # html_content = generate_html_recursive(data_json, color_json, [])
    # html_content = generate_html_recursive_v2(data_json, color_json)
    html_content = generate_html_recursive_v4(d1, color_json, d2, color_json)
    final_html = f'<pre>{{\n{html_content}\n}}</pre>'
    return final_html



data_json1 = {
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

data_json2 = {
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

color_json = {
    "A": {
        "B2": "Red",
        "B3": "Green",
        "B4": {
            "C2": "Red",
            "C3": "Green",
            "C4": "Yellow",
            "C5": "Green"
        },
        "B5": "Yellow"
    },
    "AL2": "Yellow",
    "AL3": "Yellow",
    "AL4": "Yellow"
}

# html_output_1 = generate_html(data_json1, color_json)
# html_output_2 = generate_html(data_json2, color_json)
# boxed_html_output_1 = f'<div style="width: 50%; border: 1px solid #000; padding: 10px;">{html_output_1}</div>'
# boxed_html_output_2 = f'<div style="width: 50%; border: 1px solid #000; padding: 10px;">{html_output_2}</div>'

# side_by_side_html = f'<div style="display: flex; width: 100%;">\n{boxed_html_output_1}\n{boxed_html_output_2}\n</div>'

side_by_side_html = generate_html(data_json1, data_json2, color_json)

# Save the combined HTML content to a file
with open("sediff_output.html", "w") as html_file:
    html_file.write(side_by_side_html)

