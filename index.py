# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.plotly as py
from dash.dependencies import Input, Output, State

from plotly import tools
import plotly.graph_objs as go

from src.components.dataPokemon import dfPokemon, dfPokemonTable
from src.components.tab1.view import renderIsiTab1, generate_table
from src.components.tab2.view import listGoFunc, generateValuePlot


from src.components.tab1.callbacks import callback_sorting_table, callback_filter_table


# res= requests.get('http://api-pokemon-baron.herokuapp.com/pokemon')
# dfPokemon = pd.DataFrame(res.json(), columns = res.json()[0].keys())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# dfPokemon = pd.read_csv('PokemonLengkap.csv')

app = dash.Dash(__name__)
server = app.server


app.title = 'Dashboard pokemon'

app.layout = html.Div([ 
    html.Center([
    html.H1('Dashboard Pokemon'),
    html.H3('''
        Created by: me
        ''')
    ]),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Data Pokemon', value='tab-1', children=renderIsiTab1()),
        dcc.Tab(label='Categorical plot', value='tab-2', children =[
            html.Div(children=[
                html.Div(children=[
                        html.P('Jenis :'), 
                        dcc.Dropdown(
                        id='jenisplotcategory',
                        options=[{'label': i, 'value': i} for i in ['Bar','Box','Violin']],
                        value='Bar'
                        )
                    ], className = 'col-3'),
                    html.Div(children=[
                        html.P('X :'), 
                        dcc.Dropdown(
                        id='xplotcategory',
                        options=[{'label': i, 'value': i} for i in ['Generation','Type 1','Type 2']],
                        value='Generation'
            )
                    ], className = 'col-3'),
                    html.Div(children=[
                        html.P('Y :'), 
                        dcc.Dropdown(
                        id='yplotcategory',
                        options=[{'label': i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='HP'
            )
            ], className = 'col-3'), 
             html.Div(children=[
                        html.P('Stats :'), 
                        dcc.Dropdown(
                        id='statsplotcategory',
                        options=[i for i in [{'label': 'Mean', 'value': 'mean'},
                                             {'label': 'Median', 'value': '50%'},
                                             {'label': 'Standard Deviation', 'value': 'std'},
                                             {'label': 'Count', 'value': 'count'},
                                             {'label': 'Min', 'value': 'min'},
                                             {'label': 'Max', 'value': 'max'},
                                             {'label': '25th percentile', 'value': '25%'},
                                             {'label': '75th percentile', 'value': '75%'}]],
                        value='mean', 
                        disabled = True
            )
            ], className = 'col-3')
        ], className = 'row'),
        html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id='categorygraph'    
            ) 
        ]), 
        
        dcc.Tab(label='Scatter Plot', value='tab-3', children=[
            html.Div(children=[
                html.Div(children=[
                        html.P('Hue  :'), 
                        dcc.Dropdown(
                            id='hueplotscatter',
                            options=[{'label': i, 'value': i} for i in ['Legendary','Generation','Type 1', 'Type 2']],
                            value='Legendary'
                        )
                    ], className = 'col-4'),
                    html.Div(children=[
                        html.P('X :'), 
                        dcc.Dropdown(
                            id='xplotscatter',
                            options=[{'label': i, 'value': i} for i in dfPokemon.columns[4:11]],
                            value='Attack'
            )
                    ], className = 'col-4'),
                    html.Div(children=[
                        html.P('Y :'), 
                        dcc.Dropdown(
                            id='yplotscatter',
                            options=[{'label': i, 'value': i} for i in dfPokemon.columns[4:11]],
                            value='HP'
            )
            ], className = 'col-4') 
        ], className = 'row'),
        html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id ='scattergraph'
            )    
        ]), 
        dcc.Tab(label='Pie Chart', value='tab-4', children=[
            html.Div(children=[
                        html.P('Group :'), 
                        dcc.Dropdown(
                            id='groupplotpie',
                            options=[{'label':i, 'value':i} for i in ['Legendary','Generation', 'Type 1', 'Type 2']],
                            value='Legendary'
            )], className ='col-4'),
           dcc.Graph( 
               id = 'piegraph'
            
            )]
        ),
        dcc.Tab(label ='Histogram', value='tab-5', children=[
            html.Div(children =[
                html.Div(children=[
                    html.P('Column :'),
                    dcc.Dropdown(
                    id = 'histcolumn',
                    options = [{'label':i, 'value':i} for i in list(dfPokemon.columns[4:11])],
                    value='Total'
                )
            ], className = 'col-3'),
            html.Div(children=[
                html.P('Hue: '),
                dcc.Dropdown(
                    id = 'histhue',
                    options = [{'label': 'All', 'value': 'All'}, 
                               {'label': 'Generation', 'value':'Generation'},
                               {'label': 'Legendary', 'value': 'Legendary'}],
                    value = 'All'
                )
            ], className = 'col-3'),
            html.Div(children=[
                html.P('Standard Deviation: '),
                dcc.Dropdown(
                    id = 'histstd',
                    options = [{'label': '1 Standard Deviation', 'value': 1}, 
                               {'label': '2 Standard Deviation', 'value': 2},
                               {'label': '3 Standard Deviation', 'value': 3}],
                    value = 2
                )
            ], className = 'col-3')
            ], className='row'),
            dcc.Graph(
                id='histgraph'    
            )]
        )],
    style = {
                'fontFamily': 'system-ui'
    }, content_style = {
        'fontFamily': 'Arial',
        'borderBottom': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'padding': '44px'
    }) 
], style ={
        'maxWidth': '1200px',
        'margin': '0 auto'
    }) 

#Table callback

@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "pagination_settings"),
     Input('table-multicol-sorting', "sorting_settings")])
def update_sort_paging_table(pagination_settings, sorting_settings):
    return callback_sorting_table(pagination_settings, sorting_settings)
    

@app.callback(
    Output(component_id='tablediv', component_property='children'),
    [Input('buttonsearch', 'n_clicks'),
    Input('filterrowstable', 'value')],
    [State('filternametable', 'value'),
    State('filtergenerationtable', 'value'),
    State('filtercategorytable', 'value'),
    State('filtertotaltable', 'value')]
)
def update_table(n_clicks,maxrows, name,generation,category,total):
    return callback_filter_table(n_clicks,maxrows, name,generation,category,total)
    

# Category Graph Callback
@app.callback(
    Output(component_id= 'categorygraph', component_property = 'figure'),
    [Input(component_id='jenisplotcategory', component_property = 'value'),
    Input(component_id='xplotcategory', component_property = 'value'),
    Input(component_id='yplotcategory', component_property = 'value'), 
    Input(component_id='statsplotcategory', component_property = 'value')]
)
def update_category_graph(jenisplot, xplot, yplot, stats):
    newDict = dict(
        layout = go.Layout(
            title = '{} Plot Pokemon'.format(jenisplot),
            xaxis = {"title": f'{xplot}'},
            yaxis = {'title': f'{yplot}'},
            boxmode = 'group',
            violinmode ='group'
        ), 
        data = [ 
                listGoFunc[jenisplot](
                x = generateValuePlot('True',xplot,yplot)['x'][jenisplot],
                y = generateValuePlot('True',xplot,yplot, stats)['y'][jenisplot],
                name = 'Legendary'),
                listGoFunc[jenisplot](
                x = generateValuePlot('False',xplot,yplot)['x'][jenisplot],
                y = generateValuePlot('False',xplot,yplot, stats)['y'][jenisplot],
                name = 'Non-Legendary')
                ]
        )
    return newDict    



@app.callback(
    Output(component_id= 'statsplotcategory', component_property = 'disabled'),
    [Input(component_id='jenisplotcategory', component_property = 'value')
    ]
)
def update_disabled_stats(jenisplot):
    if(jenisplot == 'Bar'):
        return False
    return True

# Scatter graph

ScatterDict = {
    'Legendary' : {'True':'Legendary', 'False': 'Non-Legendary'},
    'Generation' : {1: '1st Generation', 2: '2nd Generation', 3: '3rd Generation', 
                    4: '4th Generation', 5: '5th Generation', 6: '6th Generation'},
    'Type 1': { i:i for i in dfPokemon['Type 1'].unique()},
    'Type 2': { i:i for i in dfPokemon['Type 2'].unique()}                
}

@app.callback(
    Output(component_id= 'scattergraph', component_property = 'figure'),
    [Input(component_id='hueplotscatter', component_property = 'value'),
    Input(component_id='xplotscatter', component_property = 'value'),
    Input(component_id='yplotscatter', component_property = 'value')
    ]
)
def update_scatter_plot(hue, x, y):
    figure = dict(
                    data=[ go.Scatter(
                                            x=dfPokemon[dfPokemon[hue]== i][x],
                                            y=dfPokemon[dfPokemon[hue]== i][y],
                                            name=ScatterDict[hue][i],
                                            mode='markers'
                                            ) for i in dfPokemon[hue].unique()
                ], 
                layout = go.Layout(
                            title = 'scatterplot pokemon',
                            xaxis = {"title": f'{x}'},
                            yaxis = {'title': f'{y}'},
                            margin={'l':40,'b':40,'t':40, 'r':10},
                            hovermode ='closest'
                        )
                    )
    return figure
# Pie graph
@app.callback(
    Output(component_id= 'piegraph', component_property = 'figure'),
    [Input(component_id='groupplotpie', component_property = 'value')]
)
def update_pie(pie):
    return dict(data=
                [
                   go.Pie(
                       labels = [ScatterDict[pie][i] for i in dfPokemon[pie].unique()],
                       values= [
                           len(dfPokemon[dfPokemon[pie] == i])
                       for i in dfPokemon[pie].unique()]
                   )
               ], layout=go.Layout(
                   title='Pie Chart Pokemon',
                   margin={'l':40, 'b':40, 't':40, 'r':10}
               ))

# histogram callback
hist_hue_col ={'All': {'rows' : 1, 'cols' : 1},
               'Generation': {'rows' : 3, 'cols':2},
               'Legendary': {'rows':1, 'cols': 2}}

@app.callback(
    Output(component_id = 'histgraph', component_property = 'figure'),
    [Input(component_id= 'histcolumn', component_property = 'value'),
    Input(component_id = 'histhue', component_property = 'value'),
    Input(component_id = 'histstd', component_property = 'value')]
)
def histogram_update(column, hue, std): 

    if hue == 'All':
        dfPokehue = dfPokemon
        outlier_per_all = round((len(dfPokehue[(dfPokehue[column] < (dfPokehue[column].mean()) - (std*dfPokehue[column].std()))
                | (dfPokehue[column] > (dfPokehue[column].mean()) + (std*dfPokehue[column].std()))][column])/(len(dfPokehue))*100), 2)
        return dict(data=[
                    go.Histogram(
                        x = dfPokehue[(dfPokehue[column] >= dfPokehue[column].mean() - std*dfPokehue[column].std())
                        & (dfPokehue[column] <= dfPokehue[column].mean() + std*dfPokehue[column].std())][column],
                        marker = dict(color = 'green'),
                        name='Normal'
                    ),
                    go.Histogram(
                        x = dfPokehue[(dfPokehue[column] < dfPokehue[column].mean() - std*dfPokehue[column].std()) 
                        | (dfPokehue[column] > dfPokehue[column].mean() + std*dfPokehue[column].std())][column],
                        marker = dict(color = 'red'),
                        name='Not-Normal'
                    )],
                layout=go.Layout(
                    title =f'Histogram {column} Stats Pokemon (Outlier {outlier_per_all}%)',
                    xaxis=dict(title=f'{column}'),
                    yaxis=dict(title='Count'), 
                    height= 400
                ))
    else:
        subplot_title = []
        Pokehue_array = dfPokemon[hue].unique().reshape(hist_hue_col[hue]['rows'], hist_hue_col[hue]['cols'])
        for i in range(1, hist_hue_col[hue]['rows']+1):
            for j in range(1, hist_hue_col[hue]['cols']+1):
                dfPokeFilter = dfPokemon[dfPokemon[hue] == Pokehue_array[i-1, j-1]]
                outlier_per = round((len(dfPokeFilter[(dfPokeFilter[column] < (dfPokeFilter[column].mean()) - (std*dfPokeFilter[column].std()))
                | (dfPokeFilter[column] > (dfPokeFilter[column].mean()) + (std*dfPokeFilter[column].std()))][column])/(len(dfPokeFilter))*100), 2)
                subplot_title.append(f'{hue} {Pokehue_array[i-1, j-1]} (Outlier {outlier_per}%)')  

        fig = tools.make_subplots(rows= hist_hue_col[hue]['rows'], cols= hist_hue_col[hue]['cols'],
         subplot_titles= tuple(subplot_title), horizontal_spacing=0.15, vertical_spacing=0.2)

        for i in range(1, hist_hue_col[hue]['rows']+1):
            for j in range(1, hist_hue_col[hue]['cols']+1):
                dfPokeFilter = dfPokemon[dfPokemon[hue] == Pokehue_array[i-1, j-1]]
                fig.append_trace(go.Histogram(
                        x = dfPokeFilter[(dfPokeFilter[column] >= (dfPokeFilter[column].mean()) - (std*dfPokeFilter[column].std()))
                        & (dfPokeFilter[column] <= (dfPokeFilter[column].mean()) + (std*dfPokeFilter[column].std()))][column],
                        marker = dict(color = 'green'),
                        name= f'Normal {hue} {Pokehue_array[i-1, j-1]}'
                    ),i , j)
                fig.append_trace(go.Histogram(
                        x = dfPokeFilter[(dfPokeFilter[column] < (dfPokeFilter[column].mean()) - (std*dfPokeFilter[column].std()))
                        | (dfPokeFilter[column] > (dfPokeFilter[column].mean()) + (std*dfPokeFilter[column].std()))][column],
                        marker = dict(color = 'red'),
                        name=f'Not-Normal {hue} {Pokehue_array[i-1, j-1]}'
                    ),i , j)
                  
        for i in range(1, len(subplot_title)+1):
            fig['layout'][f'xaxis{i}'].update(title=f'{column}')
            fig['layout'][f'yaxis{i}'].update(title='count' )     
        
        if hue == 'Generation':
            fig['layout'].update(height = 800, title = f'Histogram {column} Stats Pokemon')
        elif hue == 'Legendary':
            fig['layout'].update(height = 500, title = f'Histogram {column} Stats Pokemon')
        
        return fig
   
                
if __name__ == '__main__':
    app.run_server(debug=True)