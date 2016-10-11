##coding=utf-8
import ftplib
import os
import socket
import sys

HOST = '61.174.50.219'
DIRN = '/'
FILE = '[阳光电影www.ygdy8.com].冰川时代5：星际碰撞.BD.720p.中英双字幕.mkv'
USER_NAME = 'ygdy8'
PWD = 'ygdy8'


def DownloadFile(file_name):
    try:
        f = ftplib.FTP(HOST,'ygdy8','ygdy8',)
    except(socket.error, socket.gaierror) as e:
        print('ERROR:cannot reach',e)
        return
    print('*** Connected to host %s' % HOST)

    try:
        f.login(USER_NAME, PWD)
    except ftplib.error_perm:
        print('ERROR:cannot login USER_NAME=%s, PWD=%s' % (USER_NAME, PWD))
        f.quit()
        return
    print('*** Logined in as %s' % USER_NAME)

    try:
        f.cwd(DIRN)
    except ftplib.error_perm:
        print('ERROR:cannot CD to %s' % DIRN)
        f.quit()
        return

    try:
        file = open(file_name, 'wb')
        f.retrbinary('RETR %s' % file_name, file.write)
        file.close()

    except ftplib.error_perm:
        print('ERROR:cannot read file %s' % file_name)
        os.unlink(file_name)
        file.close()
    else:
        print('*** Downloaded %s to %s' % (file_name, os.getcwd()))
    f.quit()
    return


if __name__ == '__main__':
    DownloadFile('[阳光电影www.ygdy8.com].冰川时代5：星际碰撞.BD.720p.中英双字幕.mkv')