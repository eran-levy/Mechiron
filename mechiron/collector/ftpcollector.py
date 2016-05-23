__author__ = 'Eran Levy'

import ftplib
import os
import time
import logging


class FtpCollector(object):

    def __init__(self, folder, ftpurl, username, password):
        self._ftp_connection = None
        self._folder = folder
        self._ftpurl = ftpurl
        self._username = username
        self._password = password

    def retrieve_files(self):
        os.chdir(self._folder)
        self._connect_ftp()
        # for each file in ftp
        for filename in self._ftp_connection.nlst():
            success = True
            fhandle = open(filename, 'wb')
            # it sometimes happen that it gets disconnected, we need to retry -
            # thats why there is a success while statement
            while success:
                try:
                    logging.info("Starting RETR file: " + filename)
                    self._ftp_connection.retrbinary('RETR '+filename, fhandle.write)
                    logging.info("Download finished: "+filename)
                    success = False
                except ftplib.all_errors, e:
                    logging.error("Disconnected unexpectedly from ftp server *** Retry... Error: " + str(e))
                    success = True
                    self._connect_ftp()
                    logging.info("Reconnected FTP: " + self._username)
            fhandle.close()

    def _connect_ftp(self):
        try:
            logging.info("Connecting FTP: " + self._username)
            # default timeout set to 120 sec
            self._ftp_connection = ftplib.FTP(self._ftpurl, self._username, self._password, 120)
            self._ftp_connection.set_pasv(False)
            logging.info("Successfuly connected FTP: " + self._username)
        except ftplib.all_errors, e:
            logging.error("*** Couldnt connect... " + self._username + " , sleeping for 15 sec, Error: " + str(e))
            time.sleep(15)