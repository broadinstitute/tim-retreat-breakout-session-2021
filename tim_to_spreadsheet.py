'''Example usage
python3 tim_to_spreadsheet.py \
    credentials.json \
    1BO80MKYb5QitdG_DGlGE9TP6JYCQvwr0-Q9E-mrAUt0 \
    tim.json
'''

import sys
import json
import pygsheets


NUM_ROWS = 20


credentials = sys.argv[1]
sheet_id = sys.argv[2]
tim = sys.argv[3]

tim = json.load(open(tim))['tim']

gc = pygsheets.authorize(credentials)
sheet = gc.open_by_key(sheet_id)

for element in tim:
    print('Creating {0} worksheet'.format(element['name']))
    wk = sheet.add_worksheet(
        element['name'], rows=NUM_ROWS, cols=len(element['fields']))
    cell = pygsheets.Cell('A1', worksheet=wk)
    cell.set_value('{0}: {1}'.format(
        element['identifier'], element['description']))
    cell.set_text_format('fontSize', 12)
    cell = pygsheets.Cell('A2', worksheet=wk)
    for field in element['fields']:
        print('\tAdding {0}'.format(field['name']))
        cell.note = field['description']
        cell.set_value(field['identifier'])
        cell.set_text_format('bold', True)
        try:
            cell = cell.neighbour('right')
        except:
            continue
