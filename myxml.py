from lxml import etree
import time
# tasks = [b.items() for b in config.iterfind(".//Destination[@SaveName]")]
# attrs = [{x:y for (x,y) in task} for task in tasks] 
# print(attrs[0])
# tt = config.iterfind(".//DBFFile[@FileID]")
# print([b.items() for b in tt][0])
# print('-'*10)
# {'FileID': 'SJSGF_ZR', 'Description': '深交所股份结算信息库'}
# {'FileName': '\\\\10.100.1.41\\d$\\QSSJ\\sjs\\SJSGF.DBF', 'Description': '源文件信息'}
# {'SaveName': '\\\\10.100.1.117\\d$\\send\\T_ZHONGRONGGJ01\\@Y@M@D\\融华1号\\SJSGF.DBF', 'Description': '中融信托'}
# {'SaveName': '\\\\10.100.1.117\\d$\\send\\k0247\\光大银行\\@Y@M@D\\融华1号\\SJSGF.DBF', 'Description': '光大银行'}
# {'Description': '分拆条件'}
# {'FieldID': 'GFGDDM', 'FieldName': '证券账户', 'LinkType': 'AND', 'CompType': 'C
# OMP_EQUAL', 'FieldValue': '0899044298', 'Type': 'string'}
def get_task_from_xml(xml = 'config.xml', sysdate=''):
    config = etree.XML(open(xml,'rb').read())
    data = []
    tasks = config.xpath("//DBFFile")
    for i in range(len(tasks)):
        task = tasks[i]
        target = {}
        target['id'] = i
        target['attrib'] = {}
        target['source'] = {}
        target['destination'] = []
        target['filter'] = []
        target['attrib'].update(task.attrib)
        # print(task.attrib)
        for item in task:
            # print(item.attrib)
            if 'FileName' in item.attrib:
                target['source'].update(item.attrib)
                target['source']['FileName'] = replace_date(target['source']['FileName'])
            if 'SaveName' in item.attrib:
                destination = item.attrib
                destination['SaveName'] = replace_date(destination['SaveName'],sysdate)
                target['destination'].append(destination)
                # target['destination'].append(item.attrib)
            fields = item.xpath('Field')
            if fields:
                for field in fields:
                    target['filter'].append(field.attrib)
                    # print(field.attrib)
        data.append(target)
    return data

def replace_date(string, time_str = ''):
    month = ('1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C')
    if len(time_str)>0:
        mytime =time.strptime(time_str,"%Y%m%d") 
    else:
        mytime = time.localtime(time.time())
    year2 = time.strftime('%y',mytime)
    year4 = time.strftime('%Y',mytime)
    month1 = time.strftime('%m',mytime).lstrip('0')
    month2 = time.strftime('%m',mytime)
    day1 = time.strftime('%d',mytime).lstrip('0')
    day2 = time.strftime('%d',mytime)
    mystring = string.replace('@XM',month[int(month1)-1]+day2)
    mystring = mystring.replace('@Y',year4)
    mystring = mystring.replace('@y',year2)
    mystring = mystring.replace('@M',month2)
    mystring = mystring.replace('@m',month1)
    mystring = mystring.replace('@D',day2)
    mystring = mystring.replace('@d',day1)
    return mystring


def get_sysconfig_from_xml(xml = 'config.xml'):
    config = etree.XML(open(xml,'rb').read())
    sysconfigs = config.xpath("//sysconfig")
    sysconfig = {}
    if len(sysconfigs) > 0:
        sysconfig = sysconfigs[0].attrib
    return sysconfig

# print(replace_date('\\\\10.100.1.41\d$\QSSJ\\remote\zqjsxx.@XM'))
config = get_sysconfig_from_xml()
# mytime = time.localtime(time.time())
# mytime_str = time.strftime("%Y%m%d", mytime)
# mytime = config.get("sysdate",'')
# data = get_task_from_xml(sysdate = mytime)

if __name__ == '__main__':
    # print(len(data))
    # print(get_sysconfig_from_xml())
    # print(data[0]['id'])
    print(config)
    print(data[0])


