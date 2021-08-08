# proballer.py
import pandas as pd
import sys

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it 
this.url_template = "https://www.proballers.com/basketball/player/{PROBALLER_ID}/{PLAYER}"

def get_player_url(id,name):
    id_str = str(id)
    name = name.lower().replace(' ','-')
    url = this.url_template
    url = url.replace('{PROBALLER_ID}',id_str)
    url = url.replace('{PLAYER}',name)
    print(f"--- {url} ---")
    return url

def get_primary_table(soup,name):
    source = 'list-regular'

    tables = soup.find_all('table', class_='table')
    print(f"{source}, {len(tables)}")

    df = pd.read_html(str(tables[0]))[0]

    df['Source'] = source
    df['Name'] = name

    return df

def get_secondary_tables(soup,name):

    # valid IDs Feb 2021
    divs = soup.find_all('div', id=['list-playoff','list-european-competitions','list-international-competitions'])

    df = pd.DataFrame()

    for div in divs:
        source = div['id']

        # find table within div
        tables = div.find_all('table', class_='table')
        print(f"{source}, {len(tables)}")

        # always table zero in list
        dt = pd.read_html(str(tables[0]))[0]
        dt['Source'] = source

        df = df.append(dt,ignore_index=True)

    df['Name'] = name

    return df

def get_secondary_tables_by_class(soup,name):

    # valid IDs Feb 2021
    divs = soup.find_all('div', class_=['select-tab-1','select-tab-2','select-tab-3','select-tab-4','select-tab-5'])

    df = pd.DataFrame()

    for div in divs:
        source = div['class'].replace('select-tab-content ','')

        # find table within div
        tables = div.find_all('table', class_='table')
        print(f"{source}, {len(tables)}")

        # always table zero in list
        dt = pd.read_html(str(tables[0]))[0]
        dt['Source'] = source

        df = df.append(dt,ignore_index=True)

    df['Name'] = name

    return df