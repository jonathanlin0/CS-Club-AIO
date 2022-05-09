# console_number_input
# By: Jonathan Lin

"""
add this at the top of every python file that you want to use this class in

import console_number_input

""" 
# the purpose of this class is to modulate the function of console based questions
"""

Create the object:
<object_name> = <file_name>.<class_name>()

Main function:
<object_name>.<method names>(<parameters>)


Copy paste for this specific class
obj = console_number_input.console_number_input()
obj.num_input([], "question")

"""

from time import sleep

class console_number_input:
      
    # example method
    # called by <object_name>.add(<1st parameter>, <2nd paramater) 
    def add(self, a, b):
        return a + b

    def num_input(self, list_of_options, question):

        print("")

        try:
            list_of_options = list(list_of_options)
        except:
            return "Error: The first argument is not a list type."
        if len(list_of_options) == 0:
            return "Error: The list of options is empty."


        valid_input = False
        out = ""

        for i in range(0, len(list_of_options)):
            print("[" + str(i+1) + "]   " + list_of_options[i])
            sleep(0.2)
        out = input(question + ": ")

        while valid_input == False:
            try:
                out = int(out)
                if out < 1 or out > len(list_of_options):
                    out = input("Please input a number between 1 and " + str(len(list_of_options)) + ": ")
                else:
                    valid_input = True
            except:
                out = input("Please input a number between 1 and " + str(len(list_of_options)) + ": ")
        
        return out

  
# explicit function  
# called by <class_name>.method()    
def method():
    print("GFG")