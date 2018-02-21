
# coding: utf-8

# In[101]:


deutsch_toalign = open('german_translated.txt', encoding='utf-8', errors='ignore').read()
yiddish_toalign = open('yiddish_segmented.txt', encoding='utf-8', errors='ignore').read()
import re
deutsch_preprocessed = re.sub('\.', ' .', deutsch_toalign)
deutsch_splitted = deutsch_preprocessed.split('\n') 
yiddish_splitted = yiddish_toalign.split('\n') 
aligned = open('aligned_corpora.txt', 'w', encoding='utf-8', errors='ignore') 
for x, y in zip(yiddish_splitted, deutsch_splitted):
    if len(x) and len(y) > 10:
        print("{1}  |||  {0}".format(x.strip(), y.strip()), file = aligned)
aligned.close()

