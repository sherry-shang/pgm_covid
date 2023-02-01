import dash  # pip install dash
import networkx as nx
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import copy
import random
import dash_bootstrap_components as dbc
import pandas as pd  # pip install pandas
import plotly.express as px
import math
from app_whole import app
import re
import pandas
import plotly.graph_objects as go
from plotly.tools import mpl_to_plotly
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib
import json

with open('long_app_degene.json') as jf:
    degene_json = json.load(jf)
    jf.close()

degene_lst = []
for i in degene_json:
    if len(degene_json[i]) == 6 and not degene_json[i][0] == []:
        degene_lst.append(i)



severity = 'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?'
G = pd.read_pickle("long_cov_nx.pickle")
nodes = list(G)
#nodes.remove(severity)
nodes.sort()
#nodes.remove('Number of comorbidities: ')
#nodes.remove('Post-partum (childbirth in the last year)?')

node_dropdown1 = dcc.Dropdown(nodes,value='BMI:',id='node1')
node_dropdown2 = dcc.Dropdown(nodes,value='Sex at birth:',id='node2')
degene_dropdown = dcc.Dropdown(degene_lst, value= 'Sex at birth:',id='degene_node1')

#import base64
#with open('assets/g.pdf', 'rb') as pdf:
#    pdf_data = base64.b64encode(pdf.read()).decode('utf-8')

layout = html.Div([
        html.H6([html.H3("Please select two nodes:")], style={'textAlign': "Left"}),
          node_dropdown1
        , node_dropdown2
        ,html.H6(id='my_function')
     ,   html.Div([dcc.Graph(id="ru-my-heatmap"
                            , style={"margin-right": "auto", "margin-left": "auto", "width": "80%", "height":"600px"})]
        ),
        html.H6([html.H3("Please select one node:")], style={'textAlign': "Left"}),
        degene_dropdown,
        html.H6([html.H3("Here are the genes with the highest fold changes in each group.")], style={'textAlign': "Left"}),
        html.Div([html.ObjectEl(id = 'degene_heatmap',type='application/pdf',width='1000',height='1000')],style={ 'text-align':'center'})

    ])




@app.callback(Output('degene_heatmap','data'),
              [Input('degene_node1','value')
              ])
def update_degene(node):
    var1 = node
    var2 = 'Long_Covid'
    if '/' in var1:
        var1 = var1.replace('/',' or ')
    # f.savefig('sev_age.png')
    if '?' in var1:
        return('assets/' + var1.replace('?', '') + '_' + var2 + '.pdf')
    # f.savefig(var1.replace('?','')+'_'+var2+'.pdf',bbox_inches = 'tight')
    elif ':' in var1:
        return('assets/' + var1.replace(':',' ') + '_' + var2 + '.pdf')
    else:
        return('assets/' + var1 + '_' + var2 + '.pdf')


@app.callback(Output('ru-my-heatmap','figure'),
              [Input('node1','value'),
               Input('node2','value')
              ])
def update_figure(node11,node22):
    label_x = node11
    label_y = node22
    csv = pandas.read_csv("long_cov_out_withid.csv")
    first_node_col = list(set(csv[node11].tolist()))
    second_node_col = list(set(csv[node22].tolist()))
    first_node_col = [item for item in first_node_col if not (math.isnan(item)) == True]
    second_node_col = [item for item in second_node_col if not (math.isnan(item)) == True]
    first_node_col.sort()
    second_node_col.sort()
    if -999 in first_node_col:
        first_node_col.remove(-999)
    if -999 in second_node_col:
        second_node_col.remove(-999)
    lst1 = csv[node11].tolist()
    lst2 = csv[node22].tolist()
    if node11 == severity:
        var2_lst = []
        if 4 in first_node_col:
            var2_lst.append(4)
        if 3 in first_node_col:
            var2_lst.append(3)
        if 0 in first_node_col:
            var2_lst.append(0)
        if 1 in first_node_col:
            var2_lst.append(1)
        if 2 in first_node_col:
            var2_lst.append(2)
        first_node_col = var2_lst
    if node22 == severity:
        var2_lst = []
        if 4 in second_node_col:
            var2_lst.append(4)
        if 3 in second_node_col:
            var2_lst.append(3)
        if 0 in second_node_col:
            var2_lst.append(0)
        if 1 in second_node_col:
            var2_lst.append(1)
        if 2 in second_node_col:
            var2_lst.append(2)
        second_node_col = var2_lst
    total_num = 0
    for i in range(len(lst1)):
        if lst1[i] != -999 and lst2[i] != -999:
            total_num = total_num + 1
    z_value = []
    for num2 in second_node_col:
        lst = []
        for num1 in first_node_col:
            csv1 = csv[(csv[node11] == num1) & (csv[node22] == num2)]
            lst.append(round(csv1.shape[0]/total_num,2))
        z_value.append(lst)
    reference = pd.read_pickle("C:\\Users\\shang\\Downloads\\long_discrete_to_real(1).pickle")
    x_reference_whole = reference[node11]
    y_reference_whole = reference[node22]
    x_reference = []
    y_reference = []
    if node11 == severity:
        x_reference = ['Uninfected', 'Mild', 'Moderate', 'Severe', 'Dead']
    else:
        if first_node_col[0] == 0:
            x_naming = first_node_col
        else:
            x_naming = [i - 1 for i in first_node_col]
        for i in x_reference_whole:
            if i in x_naming:
                x_reference.append(x_reference_whole[i])

    if node22 == severity:
        y_reference = ['Uninfected', 'Mild', 'Moderate', 'Severe', 'Dead']
    else:
        if second_node_col[0] == 0:
            y_naming = second_node_col
        else:
            y_naming = [i - 1 for i in second_node_col]
        for i in y_reference_whole:
            if i in y_naming:
                y_reference.append(y_reference_whole[i])
    x_reference = list(map(str, x_reference))
    y_reference = list(map(str, y_reference))
    fig = px.imshow(z_value, color_continuous_scale=px.colors.sequential.YlOrBr, text_auto=True, aspect="auto",
                    x=x_reference, y=y_reference, labels=dict(x=label_x, y=label_y))
    fig.update_layout(title_font={'size': 27}, title_x=0.5)
    fig.update_traces(hoverongaps=False,
                      hovertemplate= node11 + " %{y}"
                                    "<br>" + node22 + " %{x}"
                                    "<br>cases : %{z}<extra></extra>"
                      )
    fig.update_coloraxes(colorbar_len= 0.5)
    return fig

@app.callback(Output('my_function','children'),
              [Input('node1','value'),
              Input('node2','value')])
def update_function(node1,node2):
    return f'Here is the the correlation between {node1} and {node2}'

'''
Number of comorbidities:  
Result of the PCR test determining the participant's COVID status
Post-partum (childbirth in the last year)?

Number of comorbidities: 
Result of the PCR test determining the participant's COVID status
Post-partum (childbirth in the last year)?
'''