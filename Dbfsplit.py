from PyQt5 import QtCore, QtWidgets
from Ui_Dbfsplit import Ui_MainWindow
# import myxml
import myxml2 as myxml
import time
import sys
import os
import log
from work_thread import Work_Thread
import datetime

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None,log=None,config={},data=[]):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.task_check = {}    # 表格里面的复选框对象
        self.task_progress = {} # 表格里面的进度条对象
        self.init()
        self.config = myxml.config
        self.data = data
        self.log = log
        self.init_sysdate2today()
        self.init_task_frame(data)
        self.signl_connect()

    def init(self):
        self.msg_label.setText('')
        self.thread_result = {}
        self.thread = []
        self.task = []

    def signl_connect(self):
        self.sysdate_dateEdit.dateChanged.connect(self.load_xml)

    def load_xml(self):
        sysdate = self.sysdate_dateEdit.date().toString("yyyyMMdd")
        self.config = myxml.get_sysconfig_from_xml('config.xml')
        self.data = myxml.get_task_from_xml('config.xml', sysdate=sysdate)
        self.init_task_frame(self.data)

    def init_sysdate2today(self):
        today = datetime.datetime.now()
        self.sysdate_dateEdit.setDateTime(today)

    def init_task_frame(self,task_list=[]):
        if len(task_list)==0:task_list = self.data
        # self.task_QTableWidget.hideColumn(0)
        rowcount = self.task_QTableWidget.rowCount()
        for i in range(rowcount):
            self.task_QTableWidget.removeRow(0)
        for task in task_list:
            taskid = task['id']
            fileid = task['attrib']['FileID']
            filename = task['attrib']['Description']
            source = task['source']['FileName']
            destination = task['destination'][0]['SaveName']
            rowcount = self.task_QTableWidget.rowCount()
            chk = QtWidgets.QCheckBox('')
            progressbar = QtWidgets.QProgressBar()
            progressbar.setMinimum(0)
            progressbar.setMaximum(100)
            progressbar.setValue(0)
            # chk.setCheckState(QtCore.Qt.Unchecked)
            chk.setCheckState(QtCore.Qt.Checked)
            self.task_check[taskid] = chk
            self.task_progress[taskid] = progressbar
            self.task_QTableWidget.insertRow(rowcount)
            self.task_QTableWidget.setItem(rowcount,0, QtWidgets.QTableWidgetItem(str(taskid)))
            self.task_QTableWidget.setCellWidget(rowcount,1,chk)
            self.task_QTableWidget.setCellWidget(rowcount,2, progressbar)
            # self.task_QTableWidget.setItem(rowcount,2, QtWidgets.QTableWidgetItem('0%'))
            self.task_QTableWidget.setItem(rowcount,3, QtWidgets.QTableWidgetItem(''))
            self.task_QTableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(''))
            self.task_QTableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(fileid))
            self.task_QTableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(filename))
            self.task_QTableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(source))
            self.task_QTableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(destination))
            self.task_QTableWidget.resizeColumnsToContents()

    def get_select_task(self):
        self.task = []
        for task in self.data:
            if self.task_check[task['id']].checkState() == QtCore.Qt.Checked:
                self.task.append(task)
        return self.task

    @QtCore.pyqtSlot()
    def on_run_pushButton_clicked(self):
        # QtWidgets.QMessageBox.critical(self, "Critical", u"错误:正则表达式错误")
        self.init()
        if self.check_thread_end():
            work = self.work(self.get_select_task())
            work.start()

    @QtCore.pyqtSlot()
    def on_stop_pushButton_clicked(self):
        for thread in self.thread:
            thread.stop()

    @QtCore.pyqtSlot()
    def on_exit_pushButton_clicked(self):
        # self.init_sysdate()
        self.close()

    @QtCore.pyqtSlot()
    def on_errorlog_PushButton_clicked(self):
        today = time.localtime(time.time())
        today = time.strftime("%Y%m%d", today)
        error_log_path = os.path.abspath('error/err.%s.log'%today)
        os.popen('notepad %s'%error_log_path)

    @QtCore.pyqtSlot()
    def on_select_pushButton_clicked(self):
        for taskid,chk in self.task_check.items():
            chk.setCheckState(QtCore.Qt.Checked)

    @QtCore.pyqtSlot()
    def on_unselect_pushButton_clicked(self):
        for taskid,chk in self.task_check.items():
            chk.setCheckState(QtCore.Qt.Unchecked)

    @QtCore.pyqtSlot(tuple)
    def update_progress(self, data_tuple):
        taskid, num = data_tuple
        self.task_progress[taskid].setValue(num)

    @QtCore.pyqtSlot(tuple)
    def update_total_records(self, data_tuple):
        taskid, num = data_tuple
        self.log.debug('[thread msg] total records:%s,%s'%data_tuple)
        self.task_QTableWidget.setItem(int(taskid),4, QtWidgets.QTableWidgetItem(str(num)))
        # self.task_progress[taskid].setValue(num)

    @QtCore.pyqtSlot(tuple)
    def update_filter_records(self, data_tuple):
        taskid, num = data_tuple
        self.log.debug('[thread msg] filter records:%s,%s'%data_tuple)
        self.task_QTableWidget.setItem(int(taskid),3, QtWidgets.QTableWidgetItem(str(num)))

    @QtCore.pyqtSlot(tuple)
    def work_thread_end(self, data_tuple):
        threadid, success = data_tuple
        self.thread_result[threadid] = success
        if 'Y' in self.config.get('autorun', 'Y').upper():
            all_thread_end = True
            self.log.debug('[thread end msg %s success: %s'%data_tuple)
            if self.check_thread_end():
                self.close()
        else:
            total_success = sum([y for (x,y) in self.thread_result.items()])
            self.msg_label.setText('任务完成！%s个任务，成功: %s个'%(len(self.task), total_success))


    def work(self, data, threadid="Work_Thread"):
        work = Work_Thread(self.log, self.config, data)
        work.setIdentity(threadid)
        work.setDaemon(True)
        work.update_progress.connect(self.update_progress)
        work.total_records.connect(self.update_total_records)
        work.filter_records.connect(self.update_filter_records)
        work.thread_end.connect(self.work_thread_end)
        self.thread_result[threadid] = -1
        self.thread.append(work)
        return work

    def check_thread_end(self):
        all_thread_end = True
        for thread, success in self.thread_result.items():
            if success < 0 :
                all_thread_end = False
        return all_thread_end



if __name__ == '__main__':
    config = myxml.config
    data = myxml.get_task_from_xml('config.xml')
    loglevel = config.get('loglevel', 'DEBUG')
    today = time.localtime(time.time())
    today = time.strftime("%Y%m%d", today)
    mylog = log.Log(filename='log/all.%s.log'%today,cmdlevel=loglevel)
    err_log = log.Log('error',filename='error/err.%s.log'%today,filelevel='error')
    mylog = mylog.addFileLog(err_log)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(data=data, config=config, log=mylog)
    window.show()
    sys.exit(app.exec_())

