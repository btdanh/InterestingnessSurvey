import sys

def readAnnotationFile(file_name): 
    association_rules = {}
    with open(file_name, "r") as text_file:
        for line in text_file:
            subStrings = line.split(":")
            rule_key = subStrings[0].strip()
            label = subStrings[1].strip()
            association_rules[rule_key] = label
    return association_rules

def writeAnnotation(file_name, association_rules):
    with open(file_name, "w") as text_file:
        for rule_key, value in association_rules.items():
            text_file.write(rule_key)
            text_file.write(':')
            text_file.write(value)
            text_file.write('\n')
            
def main(argv):
    if len(argv) < 2:
        print ('Argument is not correct!')
    else:
        
        file_name = argv[1]
        association_rules = readAnnotationFile(file_name)
        
        rule_keys = association_rules.keys()
        
        n = len(rule_keys)
        m = sum(x == 'u' for x in association_rules.values())
        print ('There are ' + str(m) + '/' + str(n) + ' patterns need to be labelled. Press s if you want to stop!')
        
        for rule_key in rule_keys:
            answer = association_rules[rule_key]
            if(answer != 'u'): continue
            print(rule_key)
            while (True):
                answer = input('Pattern is interesting? (y/n)')
                if (answer == 'y' or answer == 'n' or answer == 's'):
                    break;
            if answer == 's': break
            association_rules[rule_key] = answer
        writeAnnotation(file_name, association_rules)
        print('New labels are recoreded!!!')
        
if __name__ == '__main__':
    main(sys.argv)