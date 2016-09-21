#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Created Time: 2015/8/25 17:46:50
#author: Cactus
from PyQt5 import QtCore
from work import Task
import threading
# import time

class Work_Thread(threading.Thread, QtCore.QThread):
    update_progress = QtCore.pyqtSignal(tuple)
    total_records = QtCore.pyqtSignal(tuple)
    filter_records = QtCore.pyqtSignal(tuple)
    thread_end = QtCore.pyqtSignal(tuple)

    def __init__(self, log, config, data):
        threading.Thread.__init__(self)
        QtCore.QObject.__init__(self)
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.log = log
        self.data = data
        self.config = config
        self.identity = ''

    def split_dbf(self, task):
        if task.check_data():
            task.log.debug("task%s:%s check_data ok" %(task.id,task.fileid))
            self.update_progress.emit((task.id, 10))
            total_records = task.read_dbf(task.filefrom)
            task.log.info('task%s:%s 总记录 %s'%(task.id,task.fileid,len(total_records)))
            self.update_progress.emit((task.id, 30))
            self.total_records.emit((task.id, len(total_records)))
            mydata = task.get_dbf_data(total_records)
            self.update_progress.emit((task.id, 60))
            self.filter_records.emit((task.id, len(mydata)))
            task.log.info('task%s:%s 匹配 %s'%(task.id,task.fileid,len(mydata)))
            if task.write_local_dbf(mydata):
                task.log.debug("task%s:%s write_local_dbf ok" %(task.id,task.fileid))
                self.update_progress.emit((task.id, 80))
                if task.copy_to_destination():
                    task.log.info('task%s:%s 执行完成'%(task.id,task.fileid))
                    self.update_progress.emit((task.id, 100))
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
            task = Task(self.log, self.config, item)
            if self.split_dbf(task):
                success +=1
        self.thread_end.emit((self.identity, success))
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
    import myxml
    config = myxml.get_sysconfig_from_xml()
    data = myxml.get_task_from_xml()
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
    work.update_progress.connect(update_progress)
    work.thread_end.connect(thread_end)
    work.start()
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    b = QtWidgets.QPushButton(u"你好!")
    b.show()
    app.exec_()
