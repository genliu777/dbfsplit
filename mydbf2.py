# py3
from dbfpy import dbf
db = dbf.Dbf("sjsfw.dbf")
for rec in db[:1]:
    print(rec)
