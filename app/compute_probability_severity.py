import networkx as nx
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

import pandas as pd


def GenerateSubBayesianNetwork( g, source, target ):
    edges = set()
    all_paths = nx.all_simple_paths( g, source, target )
    for path in all_paths:
        for i in range( len( path ) - 1 ):
            edges.add( ( path[i], path[i+1] ) )
    return BayesianNetwork( list( edges ) )

severity = 'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?'
var1 = severity
var2 = 'ALT:'
g = pd.read_pickle('sev_cov_nx.pickle')
dt = pd.read_csv('cond_prob_sev.csv')
reference = pd.read_pickle("sev_discrete_to_real_new.pickle")

var1_lst = list(set(dt[var2].tolist()))
while -999 in var1_lst:
    var1_lst.remove(-999)
var1_lst.sort()

model = GenerateSubBayesianNetwork(g,var2,var1)
nodes = list(model.nodes)
cpd_lst = []
for node in nodes:
    cpd_lst.append(MaximumLikelihoodEstimator(model, dt).estimate_cpd(node))
for cpd in cpd_lst:
    model.add_cpds(cpd)

infer_non_adjust = VariableElimination(model)
for val in var1_lst:
    print(val)
    print(infer_non_adjust.query(variables=[var1], evidence={var2: val}).values)