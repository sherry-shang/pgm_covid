
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