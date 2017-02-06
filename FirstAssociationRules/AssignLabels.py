def readAnnotationFile(file_name): 
    association_rules = []   
    with open(file_name, "r") as text_file:
        for line in text_file:
            subStrings = line.split(":")
            rule_key = subStrings[0].strip()
            label = subStrings[1].strip()
            
            association_rules.append((rule_key, label))
    return association_rules

def writeAnnotation(file_name, association_rules):
    with open(file_name, "w") as text_file:
        for rule in association_rules:
            text_file.write(rule[0])
            text_file.write(':')
            text_file.write(rule[1])
            text_file.write('\n')
            
def main(argv):
    if len(argv) < 2:
        print ('Argument is not correct!')
    else:
        print ('Press s if you want to stop!!!')
        file_name = argv[1]
        association_rules = readAnnotationFile(file_name)
        
        index = 0
        n = len(association_rules)
        while index < n and not (association_rules[index][1] == 'u'):
            index += 1
            
        checker = True
        while(index < n and checker == True):
            print(association_rules[index][1])
            answer = 'u'
            while (True):
                answer = input('Is it interesting? (y/n)')
                if (answer == 'y' or answer == 'n' or answer == 's'):
                    break;
            if answer == 's':
                checker = False
            else: 
                association_rules[index][1] = answer
                index += 1
        writeAnnotation(file_name, association_rules)
        
            
            
            