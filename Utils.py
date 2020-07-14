from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
import MySQLdb as mdb
import sys


# To replace the repetitive code in the controllers
class DBUtils(object):
    def DBConnection(self):
        try:
            self.con = mdb.connect('localhost', 'root', '', 'rehab')
        except mdb.Error as e:
            QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
            sys.exit(1)

    def DBFetchJson(self, sql):
        with self.con:
            cur = con.cursor()
            cur.execute(sql)
            jsonFetchedBySQL = cur.fetchone()
            return jsonFetchedBySQL
