
for node in node_elements1:
    if node['data']['label'] == type1:
        id = node['data']['id']
        for selector in stylesheet_copy1:
            if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', id) + 'Node':
                selector['style']['background-color'] = color1
                selector['style']['shape'] = shape1
            for selector in stylesheet_hover1:
                if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', id) + 'Node':
                    selector['style']['background-color'] = color1
                    selector['style']['shape'] = shape1


for selector in stylesheet_copy1:
    if selector['selector']


'''
a = ['a','1']
b = ['b','2']
c = ['c','3']
x = input()
print(eval(x))
'''

'''
var1 = severity
var2 = dropdown
dt = pd.read_csv('cond_prob_sev.csv')
reference = pd.read_pickle("C:\\Users\\shang\\Downloads\\sev_discrete_to_real(1).pickle")
var1_lst = list(set(dt[var2].tolist()))
while -999 in var1_lst:
    var1_lst.remove(-999)
var1_lst.sort()

model = GenerateSubBayesianNetwork(G1, var2, var1)
nodes = list(model.nodes)
cpd_lst = []
for node in nodes:
    cpd_lst.append(MaximumLikelihoodEstimator(model, dt).estimate_cpd(node))
for cpd in cpd_lst:
    model.add_cpds(cpd)

infer_non_adjust = VariableElimination(model)
row_lst = []
row_lst.append(['','Severity: 0','Severity: 1','Severity: 2'])
if var1_lst[0] == 0:
    naming = var1_lst
else:
    naming = [i-1 for i in var1_lst]
for i in range(len(var1_lst)):
    print(naming)
    row_lst.append([var2 + reference[var2][naming[i]]] + infer_non_adjust.query(variables=[var1], evidence={var2: var1_lst[i]}).values)

table_body = [html.Tbody(row_lst)]

return stylesheet_copy_copy1, table_body
            '''