from PyQt5 import QtWidgets, uic
import sys
import os
import json

default_param = {"dbAddress": "localhost",
                 "dbUser": "user",
                 "dbPasswd": "passwd",
                 "redisAddress": "localhost",
                 "redisUser": "user",
                 "redisPasswd": "passwd"}

actual_param = {}

if not os.path.exists("parameters.json"):
    with open('parameters.json', 'w') as param_file:
        json.dump(default_param, param_file)
        pass
else:
    with open('parameters.json') as param_file:
        actual_param = json.load(param_file)


# (host='127.0.0.1', port=6379, db=0)
#             logger.info("REDIS 접속 성공")
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()  # call the inherited classes __init__ method
        uic.loadUi('main.ui', self)

        self.db_ip_text.setText(actual_param['dbAddress'])
        self.db_user_text.setText(actual_param['dbUser'])
        self.db_passwd_text.setText(actual_param['dbPasswd'])
        self.redis_ip_text.setText(actual_param['redisAddress'])
        self.redis_port_text.setText(actual_param['redisUser'])
        self.redis_db_name_text.setText(actual_param['redisPasswd'])

        self.save_bt.clicked.connect(self.save)
        self.reset_bt.clicked.connect(self.reset)

    def save(self):
        actual_param['dbAddress'] = self.db_ip_text.toPlainText()
        actual_param['dbUser'] = self.db_user_text.toPlainText()
        actual_param['dbPasswd'] = self.db_passwd_text.toPlainText()
        actual_param['redisAddress'] = self.redis_ip_text.toPlainText()
        actual_param['redisUser'] = self.redis_port_text.toPlainText()
        actual_param['redisPasswd'] = self.redis_db_name_text.toPlainText()

        with open('parameters.json', 'w') as param_file:
            json.dump(actual_param, param_file)

    def reset(self):
        if not os.path.exists("parameters.json"):
            with open('parameters.json', 'w') as param_file:
                json.dump(default_param, param_file)
        else:
            with open('parameters.json', 'w') as param_file:
                json.dump(default_param, param_file)

        self.db_ip_text.setText(default_param['dbAddress'])
        self.db_user_text.setText(default_param['dbUser'])
        self.db_passwd_text.setText(default_param['dbPasswd'])
        self.redis_ip_text.setText(default_param['redisAddress'])
        self.redis_port_text.setText(default_param['redisUser'])
        self.redis_db_name_text.setText(default_param['redisPasswd'])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
