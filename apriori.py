def Apriori_gen(Itemset, lenght):
    canditate = []
    canditate_index = 0
    for i in range (0,lenght):
        element = str(Itemset[i])
        for j in range (i+1,lenght):
            element1 = str(Itemset[j])
            if element[0:(len(element)-1)] == element1[0:(len(element1)-1)]:
                    unionset = element[0:(len(element)-1)]+element1[len(element1)-1]+element[len(element)-1] 
                    unionset = ''.join(sorted(unionset))  
                    canditate.append(unionset)
    return canditate

def Apriori_prune(Ck,MinSupport):
    L = []
    for i in Ck:
        if Ck[i] >= minsupport:
            L.append(i)
    return sorted(L)
def Apriori_count_subset(Canditate,Canditate_len):
    Lk = dict()
    file = open('example.txt')
    for l in file:
        l = str(l.split())
        count = 0
        for i in range (0,Canditate_len):
            key = str(Canditate[i])
            if key not in Lk:
                Lk[key] = 0
            flag = True
            for k in key:
                if k not in l:
                    flag = False
            if flag:
                Lk[key] += 1
    file.close()
    return Lk
import pandas as pd
import sqlite3
dat = sqlite3.connect('db.sqlite3')
query = "select trans_id,group_concat(prod_sku_id)from website_addtocart group by trans_id"
df = pd.read_sql_query(query,dat)
minsupport = 3
C1={} 
file = df
for line in file:
    for item in line.split():
        if item in C1:
            C1[item] +=1
        else:
            C1[item] = 1
file.close()
L = []
L1 = Apriori_prune(C1,minsupport)
L = Apriori_gen(L1,len(L1))
print ('Frequent 1-itemset is',L1)
k=2
while L != []:
    C = dict()
    C = Apriori_count_subset(L,len(L))
    fruquent_itemset = []
    fruquent_itemset = Apriori_prune(C,minsupport)
    print ('Frequent',k,'-itemset is',fruquent_itemset)
    L = Apriori_gen(fruquent_itemset,len(fruquent_itemset))
    k += 1
