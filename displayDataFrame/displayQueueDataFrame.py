import pandas as pd
import re
def createHTMLDataFrameFile(df):
    # data = {
    #     'Name': ['John', 'Alice', 'Bob'],
    #     'Age': [30, 25, 35],
    #     'City': ['New York', 'Los Angeles', 'Chicago']
    # }
    # df = pd.DataFrame(data)
    html_content = df.to_html(index=False, escape=False) 
    html_content = html_content.replace('<table', '<table id="data-table"')  
    html_content = html_content.replace('<tbody>', '<tbody id="table-body">')  
    html_content = html_content.replace('</thead>', '</thead><tbody>') 
    html_content += """
    <script>
    function removeRow(button) {
        var row = button.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }
    document.addEventListener('DOMContentLoaded', function() {
        var buttons = document.querySelectorAll('.remove-button');
        buttons.forEach(function(button) {
            button.addEventListener('click', function() {
                removeRow(this);
            });
        });
    });
    </script>
    """
    html_content = html_content.replace('<tr>', '<tr class="data-row">')
    html_content = html_content.replace('</tr>', '</tr><td></td>', 1)
    html_content = html_content.replace('</tr><tr class="data-row">', '</td><td><button class="remove-button" onclick="removeRow(this)">Remove</button></td></tr><tr class="data-row">')  # Only replace the first occurrence
    pattern = r'</tr>\s*</tbody>'
    replacement = '</td><td><button class="remove-button" onclick="removeRow(this)">Remove</button></td></tr></tbody>'
    html_content = re.sub(pattern, replacement, html_content)
    pattern = r'</tr>\s*<tr class="data-row">'
    replacement = '</td><td><button class="remove-button" onclick="removeRow(this)">Remove</button></td></tr><tr class="data-row">'
    html_content = re.sub(pattern, replacement, html_content)
    with open('manualqueue.html', 'w') as file:
        file.write(html_content)