import sys
import unittest
import os
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

import utility
import json

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_interet_connection(self):
        self.assertEqual( utility.check_internet(), 200)

    def test_login(self):
        self.assertEqual( utility.make_login('qweqwe','asd456')['status'], True)

    

if __name__ == '__main__':
    unittest.main()