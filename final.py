import re
import json
import difflib
import subprocess

def get_json_diff_result(file1, file2):
    command = ["json-diff", file1, file2]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout


def func(f1, f2):
    diff_result = get_json_diff_result(f1, f2)
    print(diff_result)

    full_len_doc = generate_json_diff_html(f1, f2)
    style_regex1 = re.compile(r'<style>(.*?)<\/style>', re.DOTALL)
    style_content1 = style_regex1.search(full_len_doc).group(1)
    style_regex2 = re.compile(r'<style type="text/css">(.*?)<\/style>', re.DOTALL)
    style_content2 = style_regex2.search(full_len_doc).group(1)
    style_regex2 = re.compile(r'<body>(.*?)<\/body>', re.DOTALL)
    body_content = style_regex2.search(full_len_doc).group(1)
    print(full_len_doc)

    html_str = f'''
        <!doctype html>
        <html lang="en-us">
            <head>
                <meta charset="utf-8" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.1/styles/github.min.css" />
                <link
                rel="stylesheet"
                type="text/css"
                href="https://cdn.jsdelivr.net/npm/diff2html/bundles/css/diff2html.min.css"
                />
                <style>
                    #iframeContainer {{
                        border: 1px solid #ccc;
                        padding: 10px;
                        width: 98%;
                        margin: auto;

                    }}
                    #iframe {{
                        display: none; /* Initially hide the iframe */
                        width: 100%;
                        border: none;
                    }}
                    {style_content1}
                    {style_content2}
                </style>
                <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/diff2html/bundles/js/diff2html-ui.min.js"></script>
            </head>
            <script>
                const diffString = `--- a/{j1_json_path}\n+++ b/{j2_json_path}\n@@ -1 +1 @@\n{diff_result}`;

                document.addEventListener('DOMContentLoaded', function () {{
                var targetElement = document.getElementById('myDiffElement');
                var configuration = {{
                    drawFileList: true,
                    fileListToggle: false,
                    fileListStartVisible: false,
                    fileContentToggle: false,
                    matching: 'lines',
                    outputFormat: 'side-by-side',
                    synchronisedScroll: true,
                    highlight: true,
                    renderNothingWhenEmpty: false,
                }};
                var diff2htmlUi = new Diff2HtmlUI(targetElement, diffString, configuration);
                diff2htmlUi.draw();
                diff2htmlUi.highlightCode();
                }});

                
            </script>
            <body>
                <div id="myDiffElement"></div>
                <div id="iframeContainer">
                    <button id="toggleButton">Full Length</button>
                    <div id="iframe">
                        {body_content}
                    </div>
                </div>
                <script>
                    const toggleButton = document.getElementById('toggleButton');
                    const iframe = document.getElementById('iframe');

                    toggleButton.addEventListener('click', () => {{
                        if (iframe.style.display === 'none') {{
                            iframe.style.display = 'block';
                        }} else {{
                            iframe.style.display = 'none';
                        }}
                    }});
                </script>
            </body>
            
        </html>
    '''

    with open("diff_output.html", "w") as f:
        f.write(html_str)



def generate_json_diff_html(file1_path, file2_path):
    # Load the JSON files
    with open(file1_path) as f:
        json1 = json.load(f)

    with open(file2_path) as f:
        json2 = json.load(f)

    # Calculate the difference as text
    diff_text = difflib.ndiff(json.dumps(json1, indent=2).splitlines(), json.dumps(json2, indent=2).splitlines())

    # Generate HTML representation of the differences
    html_diff = difflib.HtmlDiff().make_file(json.dumps(json1, indent=2).splitlines(), json.dumps(json2, indent=2).splitlines())

    # Add the new legend HTML at the beginning
    new_legend_html = f'''
    <table class="diff2">
        <tbody><tr> <th colspan="2"> Legends </th> </tr>
        <tr> <td> <table border="" summary="Colors">
                  <tbody><tr><th> Colors </th> </tr>
                  <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                  <tr><td class="diff_chg">Changed</td> </tr>
                  <tr><td class="diff_sub">Deleted</td> </tr>
              </tbody></table></td>
             <td> <table border="" summary="Links">
                  <tbody><tr><th colspan="2"> Links </th> </tr>
                  <tr><td>(f)irst change</td> </tr>
                  <tr><td>(n)ext change</td> </tr>
                  <tr><td>(t)op</td> </tr>
              </tbody></table></td> </tr>
    </tbody></table>
    <div style="display: flex; justify-content: space-between; margin-top: 50px; text-transform: uppercase;">
    <div style="width: 50%; text-align: left; font-size: 20px; font-weight: bold; letter-spacing: 2px;">{'==>&nbsp;&nbsp;' + file1_path}</div>
    <div style="width: 50%; text-align: left; font-size: 20px; font-weight: bold; letter-spacing: 2px;">{'==>&nbsp;&nbsp;' + file2_path}</div>
    </div>
    '''

    html_diff = new_legend_html + html_diff

    # Add inline CSS for styling and hiding the old legend
    css = """
    <style>
      .diff { padding: 10px; width: 100%; margin-top: 10px; }
      .diff[summary="Legends"] { display: none; }
    </style>
    """
    html_diff = html_diff.replace('<head>', f'<head>{css}')
    
    return html_diff

j1_json_path = "j1.json"
j2_json_path = "j2.json"
func(j1_json_path, j2_json_path)
