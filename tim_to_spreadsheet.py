'''Example usage
python3 tim_to_spreadsheet.py \
    credentials.json \
    1BO80MKYb5QitdG_DGlGE9TP6JYCQvwr0-Q9E-mrAUt0 \
    tim.json

Where credentials.json is obtained from the broad-epi-dev project.
The second parameter is the google spreadsheet ID.

pygsheets reference: https://pygsheets.readthedocs.io/en/latest/reference.html
'''

import sys
import json
import pygsheets


NUM_ROWS = 20
CELL_COLOR = (223 / 255., 227 / 255., 235 / 255.)


credentials = sys.argv[1]
sheet_id = sys.argv[2]
tim = sys.argv[3]

tim = json.load(open(tim))['tim']

# Triggers OAuth flow
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
        cell.color = CELL_COLOR
        cell.set_value(field['identifier'])
        cell.set_text_format('bold', True)
        try:
            cell = cell.neighbour('right')
        except:
            continue
