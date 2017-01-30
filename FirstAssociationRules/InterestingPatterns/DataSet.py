import csv

# Transaction databases, each transaction is a set of items
class DataSet:
    def __init__(self):
        self.current = 0
        self.data = []
    
    def __iter__(self):
        return iter(self.data)
                
    def size(self):
        return len(self.data)
    
    def getTransaction(self, index):
        return self.data[index]
        
    # The input file should be formatted in CSV (comma separated)
    def loadInHorizontalFormat(self, file_path):
        self.data = []
        with open(file_path, 'rt') as fReader:
            reader = csv.reader(fReader)
            temp_list = list(reader)
            for transaction in temp_list:
                self.data.append(set(transaction))
            
    def loadInVerticalFormat(self, file_path):
        self.data = []
        transaction_dict = {}
        with open(file_path, 'rt') as fReader:
            reader = csv.reader(fReader)
            temp_list = list(reader)
            
            for line in temp_list:
                if len(line) < 2:
                    continue
                transaction_name = line[1]
                if transaction_name in transaction_dict:
                    transaction_dict[transaction_name].append(line[0])
                else:
                    transaction_dict[transaction_name] = []
                    transaction_dict[transaction_name].append(line[0])
            #Copy item sets
            for value in transaction_dict.values():
                self.data.append(set(value))