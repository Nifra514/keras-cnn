import sys
import unittest
import os
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
import utility
import json

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_interet_connection(self):
        self.assertEqual( utility.check_internet(), 200)

    def test_login(self):
        self.assertEqual( utility.make_login('qweqwe','asd456')['status'], True)

    
    def test_logout(self):
        self.assertEqual( utility.logout(),True)

    def test_write_log(self):
        self.assertEqual( utility.write_log(0,'test','test data','testing','None'),True)

if __name__ == '__main__':
    unittest.main()