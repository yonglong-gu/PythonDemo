import urllib.request
import os
import base64
import time


def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()

    return html

def get_page(url):
    html = url_open(url).decode('utf-8')

    a = html.find('current-comment-page')+23
    b = html.find(']',a)

    return html[a:b]


def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []

    a = html.find('img src=')

    while a != -1:
        b = html.find('.jpg',a ,a+255)
        if b != -1:
            img_addrs.append('https:'+html[a+9:b+4]) # 'img src='为9个偏移  '.jpg'为4个偏移
        else:
            b = a+9
        a = html.find('img src=', b)

    return img_addrs


def save_imgs(folder, img_addrs):
    for each in img_addrs:
        filename = each.split('/')[-1]
        with open(filename, 'wb') as f:
            img = url_open(each)
            f.write(img)
        print(img_addrs)

def download_mm(folder = 'xxoo', pages = 86):
    os.mkdir(folder)
    os.chdir(folder)

    url = 'http://jandan.net/ooxx/'
    page_num = int(get_page(url))

    for i in range(pages):
        page_num -= i


        murl = time.strftime("%Y%m%d", time.localtime())+ '-' +str(page_num)
        str_url = base64.encodestring(murl.encode("utf-8"))
        str_url = str_url.decode("ascii")
        # str_url = base64.b64decode((time.strftime("%Y%m%d", time.localtime()) + '-' + page_num).encode("utf-8"))
        page_url = url + str_url
        # page_url = url + 'page-'+ str(page_num) + '#comments'
        img_addrs = find_imgs(page_url)
        save_imgs(folder, img_addrs)
        print('地址url----' + page_url)



if __name__ == '__main__':
    download_mm()