import os
Partnumber ="1223"
L =1
FileFolder_Ok = 'Record/' + Partnumber + '/Point' + str(L + 1) + '/OK'
path = os.path.join(FileFolder_Ok)
try:
    os.makedirs(path, exist_ok=True)
except OSError as error:
    pass
FileFolder_NG = 'Record/' + Partnumber + '/Point' + str(L + 1) + '/NG'
path = os.path.join(FileFolder_NG)
