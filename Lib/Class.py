import os
import json
Partnumber = "TBA35C9LCO"
Packing = 10


def Check_Priter(Partnumber, Packing):
    Check_File = os.path.isfile(Partnumber + '\Couter_Printer.json')
    print(Check_File)
    if Check_File == False:
        item = {"Partnumber": Partnumber, "Counter": 0, 'Packing': Packing}
        with open(Partnumber+'\Couter_Printer.json', 'w') as json_file:
            json.dump(item, json_file, indent=6)


Check_Priter(Partnumber,Packing)