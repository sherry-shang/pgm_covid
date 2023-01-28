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

severity = 'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?'
G = pd.read_pickle("sev_cov_nx.pickle")
nodes = list(G)
nodes.remove(severity)
nodes.sort()
nodes.append('severity')
#nodes.remove('Number of comorbidities: ')
#nodes.remove('Post-partum (childbirth in the last year)?')

node_dropdown1 = dcc.Dropdown(nodes,value='BMI:',id='node1')
node_dropdown2 = dcc.Dropdown(nodes,value='Weight in kg:',id='node2')

layout = html.Div([
        #html.Div([html.H3("Visualize:")], style={'textAlign': "Left"})
          node_dropdown1
        , node_dropdown2
        ,html.H6(id='my_function1')
     , html.Div([dcc.Graph(id="ru-my-heatmap1"
                            , style={"margin-right": "auto", "margin-left": "auto", "width": "80%", "height":"600px"})]
        ),
    ])

@app.callback(Output('ru-my-heatmap1','figure'),
              [Input('node1','value'),
               Input('node2','value')
              ])
def update_figure(node11,node22):
    csv = pandas.read_csv("sev_ided(1).csv")
    if node11 == 'severity':
        node11 = severity
    if node22 == 'severity':
        node22 == severity
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
    for idx, num1 in enumerate(first_node_col):
        for num2 in second_node_col:
            csv1 = csv[(csv[node11] == num1) & (csv[node22] == num2)]
            z_value.append(round(csv1.shape[0]/total_num,2))
    node1 = []
    node2 = []
    for num1 in first_node_col:
        int1 = 0
        while int1 < len(second_node_col):
            node1.append(num1)
            int1 += 1
    int2 = 0
    while int2 < len(first_node_col):
        node2 = node2 + second_node_col
        int2 += 1

    data = {
        node11: node1,
        node22: node2,
        'cases': z_value
    }
    string_list1 = list(map(str, first_node_col))
    string_list2 = list(map(str, second_node_col))
    df = pandas.DataFrame(data)
    df = df.pivot(node11, node22, 'cases')
    if len(first_node_col) == 2:
        if len(second_node_col) == 2:
            fig = px.imshow(df, color_continuous_scale=px.colors.sequential.YlOrBr, text_auto=True, x=['No','Yes'],y=['No','Yes'],aspect="auto")
        else:
            fig = px.imshow(df, color_continuous_scale=px.colors.sequential.YlOrBr, text_auto=True, y=['No', 'Yes'],x=string_list2,aspect="auto")
    elif len(second_node_col) == 2:
        fig = px.imshow(df, color_continuous_scale=px.colors.sequential.YlOrBr, text_auto=True, x=['No', 'Yes'],y=string_list1,aspect="auto")
    else:
        fig = px.imshow(df, color_continuous_scale=px.colors.sequential.YlOrBr,text_auto=True,aspect="auto",x=string_list2,y=string_list1)
    fig.update_layout(title_font={'size': 27}, title_x=0.5)
    fig.update_traces(hoverongaps=False,
                      hovertemplate= node11 + " %{y}"
                                    "<br>" + node22 + " %{x}"
                                    "<br>cases : %{z}<extra></extra>"
                      )
    fig.update_coloraxes(colorbar_len= 0.5)
    return fig

@app.callback(Output('my_function1','children'),
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