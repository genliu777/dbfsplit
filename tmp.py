# %s/\v192\.101\.3\.178\\g\$/192.168.1.104\\f$\\tmp/
import os
# if not os.path.exists('d:/abc/def'):
#     os.makedirs('d:/abc/def')
a = os.path.abspath('tmp/%s.dbf'%1)
print(a)
p = os.path.abspath('log/tmp.123')
print(p)
print(os.path.abspath('sss/%s'%os.path.basename(p)))
# path = r'\\192.101.1.227\e$\huangming\sjsfw1.DBF'
# host = path[:path.find('\\',3)]+'ipc$'
# print(host)
import dbf
path = os.path.abspath('sjsfw.dbf')
print(path.upper())
print('.DBF' not in path.upper())
# print(path)
# records = dbf.Table(path, dbf_type='db3')
# records.open()
# print(len(records))
# for record in records[:1]:
#     dbf.delete(record)
# records.pack()
# print(len(records))
# records.close()


