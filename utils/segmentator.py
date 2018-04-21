
# coding: utf-8

# In[56]:


yiddish = open('yiddish_unaligned.txt', encoding='utf-8', errors='ignore').read()
yiddish_tokenized = yiddish.split()
yiddish_onestring = ' '.join(yiddish_tokenized)
def string_reverse(str1):
    rstr1 = ''
    index = len(str1)
    while index > 0:
        rstr1 += str1[ index - 1 ]
        index = index - 1
    return rstr1
yiddish_reversed = (string_reverse(yiddish_onestring))
yiddish_reversed_tokenized = yiddish_reversed.split(".")
yiddish_segmented = open("yiddish_segmented.txt","w", encoding='utf-8', errors='ignore')
for i in yiddish_reversed_tokenized:
    print (string_reverse(i) + '\n', file = yiddish_segmented)
yiddish_segmented.close()    

