# coding: utf-8

import os
import re
import sys
import urllib2
import shutil
import socket
import subprocess
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import socket


PAGE_URL = "http://www.iqiyi.com/v_19rroonq48.html"
SWF_NAME = "MainPlayer.swf"
FDIR = os.path.dirname(os.path.abspath(__file__))
HOST = '127.0.0.1'
PORT = 8036
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'}


def download_swf():
    if os.path.exists(SWF_NAME): os.remove(SWF_NAME)
    print >> sys.stderr, "Downloading the page %s, please wait..." % PAGE_URL
    req = urllib2.Request(PAGE_URL, headers=headers)
    page = urllib2.urlopen(req).read()
    swf_url = re.compile(r'http://[^\'"]+MainPlayer[^.]+\.swf').findall(page)
    swf_url = swf_url[0]
    history(swf_url)
    print 'swf url is %s' % swf_url
    data = urllib2.urlopen(swf_url).read()
    open(SWF_NAME, "wb").write(data)
    return os.path.join(FDIR, SWF_NAME)


def patch_swf(swf):
    abc_id = '%s-0' % SWF_NAME.split('.')[0]

    try:
        os.remove('%s.abc' % abc_id)
        shutil.rmtree(abc_id)
    except:
        pass

    try:
        subprocess.check_call(['tool/abcexport.exe', '%s' % swf])
        subprocess.check_call(['tool/rabcdasm.exe', '%s.abc' % abc_id])
        subprocess.Popen(['tool/patch.exe', '-p0', '-i', '../tool/asasm.patch'], cwd=abc_id).wait()
        subprocess.check_call(['tool/rabcasm.exe', '%s/%s.main.asasm' % (abc_id, abc_id)])
        subprocess.check_call(['tool/abcreplace.exe', '%s' % swf, '0', '%s/%s.main.abc' % (abc_id, abc_id)])
        print 'Patch succeeded!'
        return True
    except:
        print 'Patch failed!'
        return False


def history(swf_url):
    filename = 'history.txt'
    cache = open(filename).read()
    his_swf = re.split("\r|\n", cache)
    if swf_url not in his_swf: open('history.txt', 'a').write(swf_url + "\n")


def run_server():
    #Read flash, put into HTTP response data
    swf_content = '''
HTTP/1.x 200 ok
Content-Type: application/x-shockwave-flash

'''
    swf_content += open(SWF_NAME, 'rb').read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(100)

    print "Serving HTTP on", HOST, "port", PORT, "..."

    while True:
        conn, addr = sock.accept()
        request = conn.recv(1024)
        method = request.split(' ')[0]
        try:
            src  = request.split(' ')[1]
        except:
            break
        if method == 'GET':
            if src == '/%s' % SWF_NAME:
                content = swf_content
            else:
                content = "Hello World!"
        elif method == 'POST':
            form = request.split('\r\n')
            entry = form[-1]
            content = entry
            if len(entry) == 32:
                print "the enc key is: %s" % entry
                os._exit(0)
        else:
            continue
        conn.sendall(content)
        conn.close()


if __name__ == '__main__':
    swf_path = download_swf()
    patch = patch_swf(swf_path)
    if patch: run_server()
