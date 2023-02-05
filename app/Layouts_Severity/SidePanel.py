import json
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app_whole import app
from Layouts_Severity import tab1, tab2
import pandas as pd
import numpy as np
import scipy.stats as ss
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import networkx as nx

def GenerateSubBayesianNetwork( g, source, target ):
    edges = set()
    max_len  = len(tab1.shortest_path1(g, source, target)) - 1
    all_paths = nx.all_simple_paths(g, source, target, cutoff = max_len)
    for path in all_paths:
        for i in range( len( path ) - 1 ):
            edges.add( ( path[i], path[i+1] ) )
    return BayesianNetwork( list( edges ) )

G1 = pd.read_pickle("sev_cov_nx.pickle")
#G1 = pd.read_pickle("C:\\Users\\86186\\Downloads\\sev_cov_nx.pickle")
with open("sev_ided_more_var_redo_sort.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
with open('sev_normsoma_q_005.json') as jsonFile:
    jsonObjectNormedsoma = json.load(jsonFile)
    jsonFile.close()
severity = 'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?'
inference_type = ['symptom_list','followup_symptom_list','comorbidity_list','demographic','treatment','lab_results','others']
color_type = ['brown','blue','green','purple','red','pink','grey']
shape_type = ['circle','diamond','triangle','star']
layout_type = ['random','grid','concentric','cola','cose','euler','spread']
#nodes = list(G)
nodes1 = list(G1)
nodes1.remove(severity)
nodes1.append('severity')
nodes1.sort()
'''
nodes.remove('Number of comorbidities: ')
nodes.remove('Post-partum (childbirth in the last year)?')
nodes.remove("Result of the PCR test determining the participant's COVID status")
nodes.remove('�ge au recrutement:')
'''
'''
nodes1.remove('If yes, specify virus: (choice=Adenovirus)')
nodes1.remove('If yes, specify virus: (choice=Metapneumovirus)')
nodes1.remove('If yes, specify virus: (choice=Parainfluenza)')
nodes1.remove('If yes: (choice=High-frequency oscillatory ventilation)')
nodes1.remove('Treatments administered: (choice=Stem cells)')
nodes1.remove('Treatments administered: (choice=Chloroquine (Aralen))')
nodes1.remove('Treatments administered: (choice=Interferon beta)')
nodes1.remove('Treatments administered: (choice=Interferon alpha)')
nodes1.remove('Treatments administered: (choice=Ribavirin)')
nodes1.remove('Sexe:') #sexe at birth
nodes1.remove('�ge au recrutement:') #乱码
#nodes1.remove(severity)
#nodes.append()
'''

multi_dropdown1 = dcc.Dropdown(nodes1, ['BMI:'],multi=False,id='dropdown1',optionHeight=80)
submit_button1 = dbc.Button("Submit",className = "btn border border-2 btn-light", n_clicks=0, id="submit-button-state1",size="sm")
#clear_button1 = dbc.Button("Clear",className = "btn btn-secondary", n_clicks=0, id="clear-button-state")
inference_type_dorpdown11 = dcc.Dropdown(inference_type,[],id='choose-inference11')
color_dropdown11 = dcc.Dropdown(color_type,[],id='choose-color11')
shape_dropdown11 = dcc.Dropdown(shape_type,[],id='choose-shape11')
customize_button11 = dbc.Button("Customize",className = "btn border border-2 btn-light", n_clicks=0, id="customize-button-state11",size="sm")
layout_dropdown1 = dcc.Dropdown(layout_type,value='cola',id='choose-layout',clearable=False)
customize_button21 = dbc.Button("Customize",className = "btn border border-2 btn-light", n_clicks=0, id="customize-button-state21",size="sm")
node_dropdown11 = dcc.Dropdown(nodes1, placeholder="Select a node",id='node_dropdown1',value='BMI:',optionHeight=80)
node_dropdown21 = dcc.Dropdown(nodes1, placeholder="Select another node",id='node_dropdown2',value='Weight in kg:',optionHeight=80)
explore_button1 = dbc.Button("Using RNA data",className = "btn border border-2 btn-light", n_clicks=0, id="explore_button",size="sm")
explore_buttonSoma = dbc.Button("Using Somalogic data",className = "btn border border-2 btn-light", n_clicks=0, id="explore_buttonSoma",size="sm")
#collapse_button11 = dbc.Button(html.I(className="fa-sharp fa-solid fa-xmark"),id="collapse-button1",n_clicks=0,className = 'btn btn-light')
collapse_button41 = dbc.Button(html.H6('Perform Hypergeometric Test :'),id="collapse-button4",n_clicks=0,color='dark')
collapse_button11 = dbc.Button(html.H6('Basic Statistics of the network :'),id="collapse-button1",n_clicks=0,color='dark')
collapse_button21 = dbc.Button(html.H6('Network inferences :'),id="collapse-button2",n_clicks=0,color='dark')
collapse_button31 = dbc.Button(html.H6('Visualization Customize :'),id="collapse-button3",n_clicks=0,color='dark')
#collapse_button21 = dbc.Button(html.I(className="bi bi-bookmark-star"),id="collapse-button2",n_clicks=0,className = 'btn btn-light')
#collapse_button31 = dbc.Button(html.I(className="bi bi-bookmark-star"),id="collapse-button3",n_clicks=0,className = 'btn btn-light')
#collapse_button41 = dbc.Button(html.I(className="bi bi-bookmark-star"),id="collapse-button4",n_clicks=0,className = 'btn btn-light')




offcanvas1 = html.Div(
    [
        dbc.Offcanvas(
        html.Div([
        #html.H6(['Basic Statistics :', collapse_button11]),
        collapse_button11,
        dbc.Collapse(dbc.Container([
        html.Small(['Number of nodes :', html.Small(str(len(G1.nodes)))]),
        dbc.Row([html.Small(['Number of edges :', html.Small(str(len(G1.edges)))])])],
        style={'border-style': 'dotted','border-radius': '5px'}),
        id="collapse1-1",
        is_open=True,
        ),
        #html.H6(['Inferences :', collapse_button21]),
        collapse_button21,
        dbc.Collapse(dbc.Container([
        html.Small('Please select your inferences :'),
        multi_dropdown1,
        submit_button1,
        dbc.Row([html.Small(id='my_output1-1',className='mt-4')]),
        dbc.Modal([dbc.ModalBody(''),dbc.ModalFooter(dbc.Button('Close', id = 'map-close',className='ms-auto',n_clicks=0))],id='map',is_open=False,scrollable=True,size='lg')
        ],
        style={'border-style': 'dotted','border-radius': '5px'}),
        id="collapse2-1",
        is_open=True,
        ),
        #html.H6(['Visualization Customize :', collapse_button31]),
        collapse_button31,
        #clear_button,
        dbc.Collapse(dbc.Container([
        html.Small(['Customize your network: Please select type of inference, color and shape']),
        inference_type_dorpdown11,
        color_dropdown11,
        shape_dropdown11,
        customize_button11,
        dbc.Row([html.Small('Please select a layout :',className='mt-4')]),
        layout_dropdown1,
        customize_button21,],
        style={'border-style': 'dotted','border-radius': '5px'}),
        id="collapse3-1",
        is_open=True,
        ),
        #html.H6(['Perform Hypergeometric Test :', collapse_button41]),
        collapse_button41,
        dbc.Collapse(dbc.Container([
        html.H6(' Please select two nodes. '),
        node_dropdown11,
        node_dropdown21,
        explore_button1,
        explore_buttonSoma,
        dbc.Row([html.Small(id='my_output11',className='mt-4')]),
        dbc.Row([html.Small(id='my_outputSoma',className='mt-4')])],
        style={'border-style': 'dotted','border-radius': '5px'}),
        id="collapse4-1",
        is_open=True,
        ),
        dbc.Container([dbc.Button('Contact Us',id="contact-us",n_clicks=0,className = 'btn btn-light',href='https://github.com/mcgilldinglab/RAMEN/issues/',target="_blank")],style={'border-style': 'groove hidden hidden hidden','margin-top' : '20px'})
        ]),

        id="offcanvas1",
        #title="Offcanvas with/without backdrop",
        is_open=True,
        scrollable=True,
        backdrop=False,
        className= 'bg-light bg-opacity-75 border border-2',
        style = {'width': '400px'}
        ),
    ],
)


layout = html.Div([
        #html.H3("Visualization of some network",
                #style={'textAlign': 'center'}),
        dbc.Row([offcanvas1,
                 dbc.Col(html.Div([dbc.Row([
            dbc.Tabs(
            [
                dbc.Tab(label="Network", tab_id="tab-1",tab_style={"marginLeft": "auto"}),
                dbc.Tab(label="Heatmap", tab_id="tab-2"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
                     html.Div(id='tabs-content1',children=tab1.layout)])
                ]), width=True)
])])

@app.callback(
    Output("offcanvas1", "is_open"),
    [Input("open-offcanvas1", "n_clicks"),
    State("offcanvas1", "is_open")]
)
def toggle_offcanvas_scrollable(n1, is_open):
    if n1:
        return not is_open
    return is_open



@app.callback(
    Output("my_output11","children"),
    [Input("explore_button","n_clicks"),
     State("node_dropdown1","value"),
     State("node_dropdown2","value")]
)
def update_nodes(n_clicks,node1,node2):
    if n_clicks :
        if node1 == 'severity':
            node1 = severity
        elif node2 == 'severity':
            node2 = severity
        lst1 = jsonObject[node1]
        lst2 = jsonObject[node2]
        if lst1 == ['len is 1'] and lst2 == ['len is 1']:
            return (f'{node1} and {node2} both has only one unique value')
        if lst1 == ['len is 1']:
            return f'{node1} has only one unique value'
        if lst2 == ['len is 1']:
            return f'{node2} has only one unique value'
        common = np.intersect1d(lst1, lst2)
        #union = np.union1d(lst1, lst2)
        pval = 1 - ss.hypergeom.cdf((common.size)-1,57900,len(lst1),len(lst2))
        print('node1:'+ node1)
        print('node2:' + node2)
        print(common.size)
        #print(union.size)
        print(len(lst1))
        print(len(lst2))
        if node1 == severity:
            return f'the p-value of severity and {node2} using RNA data is {pval}'
        elif node2 == severity:
            return f'the p-value of {node1} and severity using RNA data is {pval}'
        return f'the p-value of {node1} and {node2} using RNA data is {pval}'
    else:
        return ''

@app.callback(
    Output("my_outputSoma","children"),
    [Input("explore_buttonSoma","n_clicks"),
     State("node_dropdown1","value"),
     State("node_dropdown2","value")]
)
def update_nodes(n_clicks,node1,node2):
    if n_clicks :
        if node1 == 'severity':
            node1 = severity
        elif node2 == 'severity':
            node2 = severity
        lst1 = jsonObjectNormedsoma[node1]
        lst2 = jsonObjectNormedsoma[node2]
        if lst1 == ['len is 1'] and lst2 == ['len is 1']:
            return (f'{node1} and {node2} both has only one unique value')
        if lst1 == ['len is 1']:
            return f'{node1} has only one unique value'
        if lst2 == ['len is 1']:
            return f'{node2} has only one unique value'
        common = np.intersect1d(lst1, lst2)
        #union = np.union1d(lst1, lst2)
        pval = 1 - ss.hypergeom.cdf((common.size)-1,57900,len(lst1),len(lst2))
        print('node1:'+ node1)
        print('node2:' + node2)
        print(common.size)
        #print(union.size)
        print(len(lst1))
        print(len(lst2))
        if node1 == severity:
            return f'the p-value of severity and {node2} using Somalogic data is {pval}'
        elif node2 == severity:
            return f'the p-value of {node1} and severity using Somalogic data is {pval}'
        return f'the p-value of {node1} and {node2} using Somalogic data is {pval}'
    else:
        return ''

@app.callback(
    Output("collapse1-1", "is_open"),
    [Input("collapse-button1", "n_clicks")],
    [State("collapse1-1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse2-1", "is_open"),
    [Input("collapse-button2", "n_clicks")],
    [State("collapse2-1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse3-1", "is_open"),
    [Input("collapse-button3", "n_clicks")],
    [State("collapse3-1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse4-1", "is_open"),
    [Input("collapse-button4", "n_clicks")],
    [State("collapse4-1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("modal-body-scroll1", "is_open"),
    [
        Input("explore_button", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll1", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(Output("map",'children'),
              Output('map','is_open'),
              State('dropdown1','value'),
              Input('submit-button-state1','n_clicks'),
              Input("map-close", "n_clicks"),
              State("map", "is_open")
              )
def update_map(dropdown,n1,n2,is_open):
    #button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if n1 or n2:
        var1 = severity
        var2 = dropdown
        dt = pd.read_csv('cond_prob_sev.csv')
        reference = pd.read_pickle("sev_discrete_to_real_new.pickle")
        var1_lst = list(set(dt[var2].tolist()))
        while -999 in var1_lst:
            var1_lst.remove(-999)
        var1_lst.sort()

        model = GenerateSubBayesianNetwork(G1, var2, var1)
        nodes = list(model.nodes)
        cpd_lst = []
        if nodes == []:
            return [dbc.ModalBody("The network doesn't has the path from the node to Severity."),
                              dbc.ModalFooter(
                                       dbc.Button('Close', id = 'map-close',className='ms-auto',n_clicks=0)
                                   )], not is_open
        for node in nodes:
            cpd_lst.append(MaximumLikelihoodEstimator(model, dt).estimate_cpd(node))
        for cpd in cpd_lst:
            model.add_cpds(cpd)

        infer_non_adjust = VariableElimination(model)
        if var1_lst[0] == 0:
            naming = var1_lst
        else:
            naming = [i - 1 for i in var1_lst]
        '''
        row_lst = []
        row_lst.append(html.Tr([html.Td(''), html.Td('Severity: 0'), html.Td('Severity: 1'), html.Td('Severity: 2')]))
        if var1_lst[0] == 0:
            naming = var1_lst
        else:
            naming = [i - 1 for i in var1_lst]
        for i in range(len(var1_lst)):
            print(naming)
            temp_lst = infer_non_adjust.query(variables=[var1], evidence={var2: var1_lst[i]}).values
            temp_lst = list(map(str, temp_lst))
            temp = []
            temp.append(html.Td(var2 + str(reference[var2][naming[i]])))
            temp.append(html.Td(x for x in temp_lst))
            row_lst.append(html.Tr(temp))
        '''
        dict1 = {}
        sub_naming = [reference[var2][naming[i]] for i in range(len(var1_lst))]
        if type(sub_naming[0]) == tuple:
            for i in range(len(sub_naming)):
                sub_naming[i] = str(tuple(round(float(x),2) for x in sub_naming[i]))
        dict1[''] = [var2 + " " + x for x in sub_naming]
        dict1['Severity: Mild'] = []
        dict1['Severity: Moderate'] = []
        dict1['Severity:Severe'] = []
        for i in var1_lst:
            lst = list(map(str,[round(float(i),2) for i in infer_non_adjust.query(variables=[var1], evidence={var2: i}).values]))
            dict1['Severity: Moderate'].append(lst[0])
            dict1['Severity: Mild'].append(lst[2])
            dict1['Severity:Severe'].append(lst[1])
        #dict1['Severity:0'] = list(map(str,[float('{:.2f}'.format(i)) for i in infer_non_adjust.query(variables=[var2], evidence={var1: 0}).values]))
        #dict1['Severity:1'] = list(map(str,[float('{:.2f}'.format(i)) for i in infer_non_adjust.query(variables=[var2], evidence={var1: 1}).values]))
        #dict1['Severity:2'] = list(map(str,[float('{:.2f}'.format(i)) for i in infer_non_adjust.query(variables=[var2], evidence={var1: 2}).values]))

        return [[dbc.ModalBody(dbc.Table.from_dataframe(pd.DataFrame(dict1))),
                              dbc.ModalFooter(
                                       dbc.Button('Close', id = 'map-close',className='ms-auto',n_clicks=0)
                                   )], not is_open]
    return [[dbc.ModalBody(''),dbc.ModalFooter(dbc.Button('Close', id = 'map-close',className='ms-auto',n_clicks=0))], is_open]

'''
@app.callback(
    Output("map", "is_open"),
    [Input('submit-button-state1', "n_clicks"), Input("map-close", "n_clicks")],
    [State("map", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
'''