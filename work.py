import shutil
import os
import dbf
# import tools


class Task():
    def __init__(self, log, config, data):
        self.log = log
        self.data = data
        self.config = config
        self.id = data['id']
        self.fileid = self.data['attrib'].get('FileID','')
        self.filename = self.data['attrib'].get('Description','')
        self.filefrom = self.data['source'].get('FileName','')
        self.fileto = self.data['destination']
        self.filter = self.data['filter']
        self.dbfs = []

    def __del__(self):
        for dbf in self.dbfs:
            dbf.close()

    def check_data(self):
        comp = {'COMP_EQUAL':lambda a,b : a==b,
                'COMP_NOTEQUAL':lambda a,b : a!=b,
                'COMP_LESS':lambda a,b : a<b,
                'COMP_NOTLESS':lambda a,b : a>=b,
                'COMP_GREAT':lambda a,b : a>b,
                'COMP_NOTGREAT':lambda a,b : a<=b}
        for filter in self.filter:
            if filter.get('LinkType','').upper() not in ['AND','OR']:
                self.log.error('task%s:%s LinkType err:%s'%(self.id,self.fileid,filter['LinkType']))
                return False
            if filter.get('CompType') not in comp:
                self.log.error('task%s:%s ComType err:%s'%(self.id,self.fileid,filter['CompType']))
                return False
        if not os.path.exists(self.filefrom):
        # if not self.check_connect(self.filefrom):
            self.log.error('task%s:%s cannot get source dbf: %s'%(self.id,self.fileid,self.filefrom))
            return False
        return True

    def check_connect(self, path, time_out=3):
        if path[1] == ':':
            return os.path.exists(path)
        host = path[:path.find('\\',3)+1]+'ipc$'
        # result = tools.command_run('net use %s >nul 2>nul'%host, time_out)
        # return result == 0

    def get_comp_result(self,record):
        comp = {'COMP_EQUAL':lambda a,b : a==b,
                'COMP_NOTEQUAL':lambda a,b : a!=b,
                'COMP_LESS':lambda a,b : a<b,
                'COMP_NOTLESS':lambda a,b : a>=b,
                'COMP_GREAT':lambda a,b : a>b,
                'COMP_NOTGREAT':lambda a,b : a<=b}
        if len(self.filter)==0: return 1
        for filter in self.filter:
            record_data = record[filter['FieldID'].lower()].strip()
            # if filter['Type'].upper() == 'STRING':
            #     filter['FieldValue'] = "'%s'"%filter['FieldValue']
            if filter['LinkType'].upper() == 'AND':
                if not comp[filter['CompType']](filter['FieldValue'],record_data):return -1
            if filter['LinkType'].upper() == 'OR':
                if comp[filter['CompType']](filter['FieldValue'],record_data):return 1
        if filter['LinkType'].upper() == 'AND':
            return 1
        if filter['LinkType'].upper() == 'OR':
            return -1

    def read_dbf(self, path):
        records = []
        if os.path.exists(path):
            records = dbf.Table(path)
            records.open()
            if records not in self.dbfs:
                self.dbfs.append(records)
        return records

    def get_dbf_data(self, records):
        # records = self.read_dbf(self.filefrom)
        mydata = [record for record in records if self.get_comp_result(record)==1]
        return mydata

    def write_local_dbf(self,data_list):
        new_records = data_list
        # if not new_records: return False
        tmp_dbf = os.path.abspath('tmp/%s.dbf'%self.id)
        if not os.path.exists('tmp'):os.mkdir('tmp')
        shutil.copy(self.filefrom, tmp_dbf)
        if not os.path.exists(tmp_dbf):
            self.log.error('task%s:%s copy %s to tmp_dbf fail:%s.dbf'%(self.id,self.fileid,self.filefrom,self.id))
            return False
        records = dbf.Table(tmp_dbf)
        records.open()
        for record in records:
            dbf.delete(record)
        records.pack()
        for record in new_records:
            records.append(record)
        records.close()
        self.log.debug('task%s:%s write %s.dbf success'%(self.id,self.fileid,self.id))
        return True

    def send_ok_file(self):
        if 'N' in self.config.get('okfile','yes').upper(): return True
        tmp_ok_file = os.path.abspath('tmp/%s.ok'%self.fileid)
        ok_file = self.fileto[0].get('SaveName','').replace('.dbf','.ok')
        ok_file = ok_file.replace('.DBF','.ok')
        self.log.debug('ok file:%s'%ok_file)
        if not os.path.exists(tmp_ok_file):
            f=open(tmp_ok_file,'w')
            f.write('')
            f.close()
        shutil.copy(tmp_ok_file, ok_file)
        # result = tools.command_run(r'copy %s %s'%(tmp_ok_file, ok_file), 3)
        if not os.path.exists(ok_file):
            self.log.error('task%s:%s copy %s to destination:%s fail'%(self.id,self.fileid,tmp_ok_file,ok_file))
            return False
        self.log.debug('task%s:%s copy %s to destination:%s success'%(self.id,self.fileid,tmp_ok_file,ok_file))
        return True

    def copy_to_destination(self):
        if 'N' in self.config.get("copyresult",'yes').upper():
            return True
        tmp_dbf = os.path.abspath('tmp/%s.dbf'%self.id)
        for destination in self.fileto:
            self.log.debug(r'copy %s %s'%(tmp_dbf, destination.get('SaveName','')))
            shutil.copy(tmp_dbf, destination.get('SaveName',''))
            # result = tools.command_run(r'copy %s %s'%(tmp_dbf, destination.get('SaveName','')), 3)
            if not os.path.exists(destination.get('SaveName','')):
                self.log.error('task%s:%s copy %s.dbf to destination:%s fail'%(self.id,self.fileid,self.id,destination.get('SaveName','')))
                return False
            self.log.debug('task%s:%s copy %s.dbf to destination:%s success'%(self.id,self.fileid,self.id,destination.get('SaveName','')))
        return True

    def work(self):
        if self.check_data():
            self.log.debug("task%s:%s check_data ok" %(self.id,self.fileid))
            total_records = self.read_dbf(self.filefrom)
            self.log.info('task%s:%s 总记录 %s'%(self.id,self.fileid,len(total_records)))
            mydata = self.get_dbf_data(total_records)
            self.log.info('task%s:%s 匹配 %s'%(self.id,self.fileid,len(mydata)))
            if self.write_local_dbf(mydata):
                self.log.info("task%s:%s write_local_dbf ok" %(self.id,self.fileid))
                if self.copy_to_destination():
                    if self.send_ok_file():
                        self.log.info('task%s:%s 执行完成'%(self.id,self.fileid))
                        return True
        return False

if __name__ == '__main__':
    import myxml
    import log
    import time
    config = myxml.get_sysconfig_from_xml()
    loglevel = config.get('loglevel','DEBUG')
    mytime = config.get('sysdate', '')
    data = myxml.get_task_from_xml(sysdate=mytime)
    today = time.localtime(time.time())
    today = time.strftime("%Y%m%d", today)
    mylog = log.Log(filename='log/all.%s.log'%today,cmdlevel=loglevel)
    err_log = log.Log('error',filename='error/err.%s.log'%today,filelevel='error')
    # err_log = log.Log('error',filename='error/err.%s.log'%today,filelevel='error',backup_count=1,when='D')
    mylog = mylog.addFileLog(err_log)
    # mylog.debug(data[0])
    t = time.time()
    success = 0
    for item in data:
        task = Task(mylog,config,item)
        if task.work():
            success += 1
        mylog.debug('task %s time used %s'%(task.id, time.time()-t))
        t = time.time()
    mylog.info('-'*25)
    mylog.info("total:%s, success:%s, fail:%s"%(len(data),success,len(data)-success))
    mylog.info('-'*25)
    if 'N' in config.get('autorun', 'yes').upper():
        os.system("pause")


