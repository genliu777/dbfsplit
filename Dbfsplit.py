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

from work import Task
from functools import partial
from multiprocessing.pool import Pool
import multiprocessing
mylog = log.Log()
config = myxml.config
def do_works(task_list):
    success = 0
    for item in task_list:
        task = Task(mylog, config, item)
        if task.work():
            success +=1
    mylog.debug('进程执行完成,成功：%s'%success)


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
        # self.threadnum = int(self.config.get('threadnum', '10'))
        self.threadnum = self.threadnum_spinBox.value()
        self.thread_list = []  # task按源文件分成多个线程
        self.show()
        if 'Y' in self.config.get('autorun', 'Y').upper():
            self.on_run_pushButton_clicked()

    def init(self):
        self.threadnum = self.threadnum_spinBox.value()
        self.msg_label.setText('')
        self.thread_result = {}  # taskid:success
        self.thread = []         # 每启动一个线程就放进来，用于停止所有线程操作
        self.task_select = []    # 存储选中的task

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
        self.task_select = []
        for task in self.data:
            if self.task_check[task['id']].checkState() == QtCore.Qt.Checked:
                self.task_select.append(task)
        return self.task_select

    def sort_data(self,task_list):
        dict_list = {}
        for task in task_list:
            if task['source']['FileName'] not in dict_list:
                # task_dict = {task['source']['FileName']:[task]}
                dict_list[task['source']['FileName']] = [task]
            else:
                new_list = dict_list[task['source']['FileName']]
                new_list.append(task)
                dict_list[task['source']['FileName']] = new_list
        return dict_list

    @QtCore.pyqtSlot()
    def on_run_pushButton_clicked(self):
        # QtWidgets.QMessageBox.critical(self, "Critical", u"错误:正则表达式错误")
        self.init()
        select_task = self.get_select_task()
        self.thread_list = [(source,task_thread) for source,task_thread in self.sort_data(select_task).items()]
        self.log.debug('len thread_list:%s'%len(self.thread_list))
        for i in range(5):
            p = multiprocessing.Process(target = do_works, args = [self.thread_list.pop(0)[1]])
            p.start()
        if self.check_thread_end():
            for i in range(self.threadnum):
                if self.thread_list:
                    source,task_thread = self.thread_list.pop()
                    work = self.work(task_thread,source)
                    work.start()

    @QtCore.pyqtSlot()
    def on_stop_pushButton_clicked(self):
        self.msg_label.setText('正在停止线程...')
        for thread in self.thread:
            thread.stop()

    @QtCore.pyqtSlot()
    def on_exit_pushButton_clicked(self):
        # self.init_sysdate()
        self.close()

    @QtCore.pyqtSlot()
    def on_errorlog_PushButton_clicked(self):
        try:
            today = time.localtime(time.time())
            today = time.strftime("%Y%m%d", today)
            error_log_path = os.path.abspath('error/err.%s.log'%today)
            if os.path.exists(error_log_path):
                os.popen('notepad %s'%error_log_path)
        except:
            self.log.trace()

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
        status = {5:'任务开始',10:'参数校验成功',30:'读取源文件dbf成功',60:'写本地dbf成功',80:'拷贝到目的地成功',100:'发送ok文件成功,任务结束'}
        taskid, num = data_tuple
        self.task_progress[taskid].setValue(num)
        self.statusBar().showMessage('线程[%s]正在处理: 任务%s,当前状态进程%s'%(self.task_QTableWidget.item(int(taskid),7).text(), taskid, status[num]))

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
        if self.msg_label.text() != '正在停止线程...':
            total_success = sum([y for (x,y) in self.thread_result.items() if y>0])
            self.msg_label.setText('已完成: %s个任务'%total_success)
            if len(self.thread_list)>0:
                source,task_thread = self.thread_list.pop()
                work = self.work(task_thread,source)
                work.start()
        else:
            self.statusBar().showMessage('线程[%s]结束'%threadid)
        if self.check_thread_end():
            if 'Y' in self.config.get('autorun', 'Y').upper():
                self.log.debug('[thread end msg %s success: %s'%data_tuple)
                self.close()
            else:
                total_success = sum([y for (x,y) in self.thread_result.items() if y >0])
                self.msg_label.setText('任务完成！%s个任务，成功: %s个'%(len(self.task_select), total_success))
                self.statusBar().showMessage('结束')


    def work(self, data, threadid="Work_Thread"):
        work = Work_Thread(self.log, self.config, data)
        work.setIdentity(threadid)
        work.setDaemon(True)
        work.msg_update_progress.connect(self.update_progress)
        work.msg_total_records.connect(self.update_total_records)
        work.msg_filter_records.connect(self.update_filter_records)
        work.msg_thread_end.connect(self.work_thread_end)
        self.thread_result[threadid] = -2
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
    # window.show()
    sys.exit(app.exec_())

