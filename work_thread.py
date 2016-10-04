#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Created Time: 2015/8/25 17:46:50
#author: Cactus
from PyQt5 import QtCore
from work import Task
import threading
# import time

class Work_Thread(threading.Thread, QtCore.QThread):
    msg_update_progress = QtCore.pyqtSignal(tuple)
    msg_total_records = QtCore.pyqtSignal(tuple)
    msg_filter_records = QtCore.pyqtSignal(tuple)
    msg_thread_end = QtCore.pyqtSignal(tuple)

    def __init__(self, log, config, data):
        threading.Thread.__init__(self)
        QtCore.QObject.__init__(self)
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.log = log
        self.data = data
        self.config = config
        self.identity = ''
        self.total_records = []
        self.total_records_num = 0

    def split_dbf_by_del(self, task):
        self.msg_update_progress.emit((task.id, 5))
        if task.check_data():
            task.log.debug("task%s:%s check_data ok" %(task.id,task.fileid))
            self.msg_update_progress.emit((task.id, 10))
            total_records = task.get_total_records()
            if total_records == False: return False
            total_records_num = len(total_records)
            task.log.info('task%s:%s 总记录 %s'%(task.id,task.fileid,total_records_num))
            self.msg_update_progress.emit((task.id, 30))
            self.msg_total_records.emit((task.id, total_records_num))
            select_records_num = task.write_local_dbf_by_del(total_records)
            self.msg_update_progress.emit((task.id, 60))
            self.msg_filter_records.emit((task.id, select_records_num))
            task.log.info('task%s:%s 匹配 %s'%(task.id,task.fileid,select_records_num))
            task.log.debug("task%s:%s write_local_dbf ok" %(task.id,task.fileid))
            if task.copy_to_destination():
                self.msg_update_progress.emit((task.id, 80))
                if task.send_ok_file():
                    task.log.info('task%s:%s 执行完成'%(task.id,task.fileid))
                    self.msg_update_progress.emit((task.id, 100))
                    return True
        return False

    def split_dbf_by_append(self, task):
        self.msg_update_progress.emit((task.id, 5))
        if task.check_data():
            task.log.debug("task%s:%s check_data ok" %(task.id,task.fileid))
            self.msg_update_progress.emit((task.id, 10))
            if self.total_records:
                total_records = self.total_records
                total_records_num = self.total_records_num
            else:
                total_records = task.read_dbf()
                if total_records == False: return False
                total_records_num = len(total_records)
                self.total_records_num = total_records_num
            task.log.info('task%s:%s 总记录 %s'%(task.id,task.fileid,total_records_num))
            self.msg_update_progress.emit((task.id, 30))
            self.msg_total_records.emit((task.id, total_records_num))
            if not task.write_local_dbf_by_append(total_records):
                task.log.debug("task%s:%s write_local_dbf fail" %(task.id,task.fileid))
                return False
            self.msg_update_progress.emit((task.id, 60))
            select_records = task.get_dbf_data(total_records)
            select_records_num = len(select_records)
            self.msg_filter_records.emit((task.id, select_records_num))
            task.log.info('task%s:%s 匹配 %s'%(task.id,task.fileid,select_records_num))
            task.log.debug("task%s:%s write_local_dbf ok" %(task.id,task.fileid))
            if task.copy_to_destination():
                self.msg_update_progress.emit((task.id, 80))
                if task.send_ok_file():
                    task.log.info('task%s:%s 执行完成'%(task.id,task.fileid))
                    self.msg_update_progress.emit((task.id, 100))
                    return True
        return False

    def stop(self):
       self.timeToQuit.set()
       self.log.debug('thread %s stop' % self.identity)

    def setIdentity(self, text):
        self.identity = text

    def work(self):
        self.log.debug('thread %s work begin' % self.identity)
        success = 0
        for item in self.data:
            if self.timeToQuit.isSet():
                break
            task = Task(self.log, self.config, item)
            if self.split_dbf_by_append(task):
                success +=1
        if self.timeToQuit.isSet():
            self.log.debug('thread %s stop by user' % self.identity)
        self.msg_thread_end.emit((self.identity, success))
        self.log.debug('thread %s work end' % self.identity)

    def run(self):
        self.log.debug('thread %s bugin' % self.identity)
        try:
            self.work()
        except:
            self.log.trace()


if __name__ == '__main__':
    import log
    import os
    # import myxml
    # config = myxml.get_sysconfig_from_xml()
    # data = myxml.get_task_from_xml()
    import myxml2
    config = myxml2.get_sysconfig_from_xml()
    data = myxml2.get_task_from_xml()
    mylog = log.Log()
    @QtCore.pyqtSlot(tuple)
    def thread_end(data):
        mylog.debug(data)
    @QtCore.pyqtSlot(tuple)
    def update_progress(data):
        mylog.debug(data)
    work = Work_Thread(mylog, config, data)
    work.setIdentity("Work_Thread")
    work.setDaemon(True)
    work.msg_update_progress.connect(update_progress)
    work.msg_thread_end.connect(thread_end)
    work.start()
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    b = QtWidgets.QPushButton(u"你好!")
    b.show()
    app.exec_()
