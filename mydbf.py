# py3
import dbf
import os
import time

sjsfw = dbf.Table('sjsfw.dbf')
sjsfw.open()
sjsfw.open()
# sjsfw.close()
# sjsfw.close()
# print('ok')
# print(type(sjsfw[0]))
# print(sjsfw[1].fwgddm)
# nd_index = table.create_index(lambda rec: (rec.name, rec.desc))
mydata = dbf.pql(sjsfw,"select * where fwgddm=='0050851437'")
# mydata = sjsfw.query("select * where fwgddm=='0050851437'")
mylist = [rec for rec in sjsfw if rec['fwjsdm'] == '0050851437']
print(mydata[0])
print(mylist[0])
import shutil
shutil.copy('sjsfw.dbf',  'sjsfw_1.dbf')
sjsfw = dbf.Table('sjsfw_1.dbf')
sjsfw.open()
for table in sjsfw:
    dbf.delete(table)
sjsfw.pack()
sjsfw.close()

"create a dbf and vfp table"
# dbf_table = dbf.Table(
#     'temptable_1',
#     'name C(30); age N(3,0); birth D' , dbf_type='db3'
#     )
# dbf_table.open()
# # t1= time.clock()
# # print(t1)
# for i in range(1000):
#     for datum in (
#             ('John Doe', 31, dbf.Date(1979, 9,13)),
#             ('Ethan Furman', 102, dbf.Date(1909, 4, 1)),
#             ('Jane Smith', 57, dbf.Date(1954, 7, 2)),
#             ('John Adams', 44, dbf.Date(1967, 1, 9)),
#             ):
#         dbf_table.append(datum)
# dbf_table.close()
# print(time.clock()-t1)
