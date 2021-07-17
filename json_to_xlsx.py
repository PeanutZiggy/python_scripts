import pandas as pd
import json

with open('task.json', encoding='utf-8') as f:
    data = json.load(f)

dff = pd.DataFrame(data.get('records'))

dff = dff.T
dff = dff.T
dff = dff.set_index('parent')

# this writer is included so that excel would not ignore the long urls
writer = pd.ExcelWriter(r'test.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
dff.to_excel(writer)
writer.close()