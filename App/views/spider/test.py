import json
import zipfile
from io import BytesIO, StringIO

# ff = StringIO()
# import pickle
# data ={
#     'status':200,
#     'msg':'ok'
# }
#
# with open('1.json','w') as f:
#     json.dump(data,f)
#
# # pickle.dump(data,ff)
#
# json.dump(data,ff)

buff = BytesIO()
zip_archive = zipfile.ZipFile(buff, mode='w')
temp = StringIO()
temp.write('sunck is a good man')
zip_archive.writestr('1.zip', temp.getvalue())
print(buff.getvalue())