import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from difflib import SequenceMatcher as SM
df = pd.read_csv(r'C:\Users\Yasharth\Desktop\cluster.csv')
df2 = pd.read_csv(r'C:\Users\Yasharth\Desktop\dataset.csv')
#creating dictionaries for one to one classification 
df1 = df2.set_index('names')
dict1 = df1.to_dict()['class']
dict2 = df1.to_dict()['brand_id']
dict3 = df1.to_dict()['sub_category']
df1 = df.set_index('products')
probrand = df1.to_dict()['brand']
prosubcat = df1.to_dict()['subcat']
procat = df1.to_dict()['cat']
query = input("enter your query here")
#following procedure is for data cleaning
sr = stopwords.words('english')
counter=0
updatestring = nltk.tag.pos_tag(query.split())
update2string = [word for word,tag in updatestring if tag=='NN']
update2string.extend([word for word,tag in updatestring if tag=='NNS'])
newstring = (' '.join(update2string))
tokens = list(word_tokenize(newstring))
clean_tokens = tokens[:]
for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)
output=[]
backup=[]
finaltokens=[]
finaloutput=[]
finaloutput2=[]
twobrands=[]
twoproducts=[]
#now we apply similarity algorithm for syntax correction
for i in clean_tokens:
    for j in dict1:
        s1 = str(i)
        s2 = str(j)
        a = SM(None,s1,s2).ratio()
        if a>=0.8:
            output.append(dict1[j])
            finaltokens.append(j)
counter1=0
#now we check for category->subcategory->brand->product sequentially and cluster items accordingly
for i,v in enumerate(output):
    if v=='sub_category':
        counter1+=1
        a = i
        b = str(finaltokens[a])
        for key in prosubcat.keys():
            if prosubcat[key]==str(b):
                finaloutput.append(key)
                finaloutput2.append(key)
    
for i,v in enumerate(output):
    if v=='brand':
        if len(finaloutput2)==0:
            a = i
            b = str(finaltokens[a])
            for key in probrand.keys():
                if probrand[key]==b:
                    finaloutput2.append(str(key))
                    finaloutput.append(str(key))
                    twobrands.append(str(key))
                    
        else:
            a = i
            b = str(finaltokens[a])
            finaloutput2 = finaloutput.copy()
            for key in probrand.keys():
                if probrand[key]==b:
                    twobrands.append(str(key))
            for m in finaloutput:
                d = probrand[str(m)]
                if d==b:
                    backup.append(str(m))
                else:
                    finaloutput2.remove(str(m))
#making finaloutput and finaloutput2 same
temp = finaloutput.copy()
for j in finaloutput:
    if j in finaloutput2:
        pass
    else:
        temp.remove(str(j))
finaloutput = temp
##

a=finaloutput2.copy()

productlist = []
for i,v in enumerate(output):
    if v=='product':
        counter+=1
        if len(finaloutput2)==0:
            a = i
            b=str(finaltokens[a])
            productlist.append(b)
            finaloutput2.append(b)
            twoproducts.append(b)
        else:
            a = i
            b=str(finaltokens[a])
            productlist.append(b)
if counter==0:
    if counter1==0:
        print(twobrands)
    else:
        if len(finaloutput2)==0:
            print('please check your search parameters')
        else:
            if len(backup)==0:
                print(finaloutput2)
            else:
                
                print(list(set(backup)))
else:
    if len(productlist)==0:
        print('please check your seacrh parameters')
    else:
        print(list(set(productlist)))

        

        
            
        
        
