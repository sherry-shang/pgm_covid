import json
import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
with open('long_app_degene.json') as jf:
    degene_json = json.load(jf)
    jf.close()
reference = pd.read_pickle("long_discrete_to_real(1).pickle")
#clinical1  = pd.read_csv('C:\\Users\\shang\\PycharmProjects\\draw\\long_cov_out_withid_in_rna.csv')
degene_lst = []
for i in degene_json:
    if len(degene_json[i]) == 6 and not degene_json[i][0] == []:
        degene_lst.append(i)
#degene_lst = ['Sex at birth:']
for node in degene_lst:
    print(node)
    norm = matplotlib.colors.Normalize(vmin=-4, vmax=4)
    var1 = node
    var2 = 'Long_Covid'
    whole_degene_lst = degene_json[node]
    lst = whole_degene_lst[0]
    var1_lst = list(set(clinical1[node].tolist()))
    while -999 in var1_lst:
        var1_lst.remove(-999)
    var1_lst.sort()
    print(var1_lst)
    reference_lst = []
    reference_lst_whole =[]
    #print(node in reference)
    #print(reference[node])
    if node in reference:
        reference_lst_whole = reference[node]
        if node in ['Number of comorbidities: ','Other immunosuppressive medications?']:
            for i in reference_lst_whole:
                if i in var1_lst:
                    reference_lst.append(node + str(reference_lst_whole[i]))
        elif len(reference_lst_whole) == len(var1_lst):
            for i in reference_lst_whole:
                reference_lst.append(node + str(reference_lst_whole[i]))
        else:
            for i in reference_lst_whole:
                if i + 1 in var1_lst:
                    reference_lst.append(node + str(reference_lst_whole[i]))
    else:
        for i in var1_lst:
            reference_lst.append(node + str(i))
    print(reference_lst)
    for i in range(len(lst)):
        l = (lst[i] - np.mean(lst[i])) / np.std(lst[i])
        lst[i] = l
    lsta = whole_degene_lst[1]

    df = pd.DataFrame(lst, index=lsta)

    lst2 = whole_degene_lst[2]

    for i in range(len(lst2)):
        l = (lst2[i] - np.mean(lst2[i])) / np.std(lst2[i])
        lst2[i] = l
    lstb = whole_degene_lst[3]

    df2 = pd.DataFrame(lst2, index=lstb)

    lst3 = whole_degene_lst[4]

    for i in range(len(lst3)):
        l = (lst3[i] - np.mean(lst3[i])) / np.std(lst3[i])
        lst3[i] = l
    lstc = whole_degene_lst[5]

    df3 = pd.DataFrame(lst3, index=lstc)

    f, axes = plt.subplots(nrows=3, sharex=True, figsize=(10, 10), constrained_layout=True)
    for ax in axes:
        ax.tick_params(labelsize=5)
        # ax.set_xticklabels(['age:21.0-31.5', 'age:31.5, 42.0', "age:42.0-52.5", 'age:52.5-63.0', 'age:63.0-73.5', 'age:73.5-84.0', 'age:84.0-94.5','Severity:Moderate','Severity:Severe','Severity:Dead','Severity:Mild'],rotation=90)
    plt.suptitle(var1 + ' vs. ' + var2)
    # plt.figure()
    sns.heatmap(data=df, ax=axes[0], cmap='bwr', norm=norm, cbar=False)
    axes[0].set_ylabel('common')

    # plt.ylabel('common de gene')
    # for tick_label in g.ax_heatmap.axes.get_yticklabels():
    #    tick_label.set_color('red')
    # plt.figure()
    sns.heatmap(data=df2, ax=axes[1], cmap='bwr', norm=norm, cbar=False)
    axes[1].set_ylabel(var1)

    # plt.figure()
    sns.heatmap(data=df3, ax=axes[2], cmap='bwr', norm=norm)
    axes[2].set_ylabel(var2)
    axes[2].set_xticklabels(
        reference_lst+['Long Covid: Non Long-COVID', 'Long Covid: Long-COVID'], rotation=20)
    # im0 = axes[0].imshow(df, vmin=1, vmax=15,cmap=sns.cubehelix_palette(as_cmap=True))
    # im1 = axes[1].imshow(df, vmin=1, vmax=15,cmap=sns.cubehelix_palette(as_cmap=True))
    # im2 = axes[2].imshow(df, vmin=1, vmax=15,cmap=sns.cubehelix_palette(as_cmap=True))
    if '/' in var1:
        var1 = var1.replace('/',' or ')
    # f.savefig('sev_age.png')
    if '?' in var1:
        f.savefig('assets/' + var1.replace('?', '') + '_' + var2 + '.jpg', bbox_inches='tight', dpi=600)
    # f.savefig(var1.replace('?','')+'_'+var2+'.pdf',bbox_inches = 'tight')
    elif ':' in var1:
        f.savefig('assets/' + var1.replace(':',' ') + '_' + var2 + '.jpg', bbox_inches='tight', dpi=600)
    else:
        f.savefig('assets/' + var1 + '_' + var2 + '.jpg', bbox_inches='tight', dpi=600)