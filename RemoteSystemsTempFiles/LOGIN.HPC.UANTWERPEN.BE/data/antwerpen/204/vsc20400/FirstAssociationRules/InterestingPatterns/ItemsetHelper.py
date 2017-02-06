def getItemsetFromKey(key):
    if key == '':
        return []
    else: 
        return key.split(',')

def createKeyFromItemset(itemset):
    return ",".join(itemset)
        
        
