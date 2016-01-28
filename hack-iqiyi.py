import os
import re
import shutil
from urllib2 import Request, urlopen
import subprocess
import socket


PAGE_URL = "http://www.iqiyi.com/v_19rroonq48.html"
SWF_NAME = "MainPlayer.swf"
HISTORY = "history.txt"
HOST = '127.0.0.1'
PORT = 8036
HEADER = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:43.0) Gecko/20100101 Firefox/43.0'}


def download_swf():
    if os.path.isfile(SWF_NAME):
        os.remove(SWF_NAME)

    try:
        print "Downloading the page %s, please wait..." % PAGE_URL
        req = Request(PAGE_URL, headers=HEADER)
        page = urlopen(req, timeout=5).read()
    except:
        print "URL open failed, please confirm PAGE_URL is exists!"
        return False

    try:
        swf_url = re.compile(r'http://[^\'"]+MainPlayer[^.]+\.swf').findall(page)[0]
        print 'swf url is %s' % swf_url
        history(swf_url)
        data = urlopen(swf_url, timeout=10).read()
        open(SWF_NAME, "wb").write(data)
        return True
    except:
        print "Download swf failed!"
        return False


def patch_swf():
    abc_path = '%s-0' % SWF_NAME.split('.')[0]
    remove_files(abc_path)

    try:
        subprocess.check_call(['tool/abcexport.exe', '%s' % SWF_NAME])
        subprocess.check_call(['tool/rabcdasm.exe', '%s.abc' % abc_path])
        subprocess.Popen(['tool/patch.exe', '-p0', '-i', '../tool/asasm.patch'], cwd=abc_path).wait()
        subprocess.check_call(['tool/rabcasm.exe', '%s/%s.main.asasm' % (abc_path, abc_path)])
        subprocess.check_call(['tool/abcreplace.exe', '%s' % SWF_NAME, '0', '%s/%s.main.abc' % (abc_path, abc_path)])
        print 'Patch succeeded!'
        remove_files(abc_path)
        return True
    except:
        print 'Patch failed!'
        return False


def history(swf_url):
    his_swf = []
    if os.path.exists(HISTORY):
        cache = open(HISTORY).read()
        his_swf = re.split("\r|\n", cache)
    if swf_url not in his_swf:
        open(HISTORY, 'a').write(swf_url + "\n")


def remove_files(abc_path):
    try:
        os.remove('%s.abc' % abc_path)
        shutil.rmtree(abc_path)
    except:
        pass


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
        try:
            method = request.split()[0]
            src  = request.split()[1]
        except:
            pass
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
    swf = download_swf()
    patch = patch_swf() if swf else False
    if patch: run_server()