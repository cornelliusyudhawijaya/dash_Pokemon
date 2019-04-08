from src.components.tab1.view import generate_table
from src.components.dataPokemon import dfPokemonTable
import pandas as pd
import requests

def callback_sorting_table(pagination_settings, sorting_settings):
    if len(sorting_settings):
        dff = dfPokemonTable.sort_values(
            [col['column_id'] for col in sorting_settings],
            ascending=[
                col['direction'] == 'asc'
                for col in sorting_settings
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = dfPokemonTable

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')

def callback_filter_table(n_clicks,maxrows, name,generation,category,total):
    global dfPokemonTable
    urlget = 'http://api-pokemon-baron.herokuapp.com/pokemon?name={}&mintotal={}&maxtotal={}'.format(name, total[0], total[1])
    if(generation != ''):
        urlget += '&generation={}'.format(generation)
    if(category != ''):
        urlget += '&legendary={}'.format(category)
    res = requests.get(urlget)
    dfPokemonTable = pd.DataFrame(res.json(), columns=res.json()[0].keys())        

    # dfFilter = dfPokemon[(dfPokemon['Name'].str.contains(name)) & ((dfPokemon['Total'] >= total[0]) & (dfPokemon['Total'] <= total[1]))]
    # if(generation != '') :
    #     dfFilter = dfFilter[dfFilter['Generation'] == int(generation)]
    # if(category != '') :
    #     dfFilter = dfFilter[dfFilter['Legendary'] == category]

    return generate_table(dfPokemonTable, pagesize=maxrows)    
