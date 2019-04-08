import plotly.graph_objs as go
from src.components.dataPokemon import dfPokemon


listGoFunc ={
    'Box' : go.Box,
    'Bar' : go.Bar,
    'Violin' : go.Violin
}

def generateValuePlot(legendary,xplot,yplot, stats='mean'):
    return{
            'x': {
            'Bar': dfPokemon[dfPokemon['Legendary']  == legendary][xplot].unique(),
            'Box': dfPokemon[dfPokemon['Legendary']  == legendary][xplot],
            'Violin': dfPokemon[dfPokemon['Legendary']  == legendary][xplot]
                },
            'y': {
            'Bar' : dfPokemon[dfPokemon['Legendary']  == legendary].groupby(xplot)[yplot].describe()[stats],
            'Box': dfPokemon[dfPokemon['Legendary']  == legendary][yplot],
            'Violin': dfPokemon[dfPokemon['Legendary']  == legendary][yplot]
            }
            }