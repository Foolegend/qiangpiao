# -*- coding:utf-8 -*-
# @Time    : 2018/4/27
# @File    : search_kugou.py
# @Software: PyCharm
# @pyVer   : python 2.7
from imp import reload

import requests,json,sys
from pip._vendor.distlib.compat import raw_input

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

headers={
        'UserAgent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
        'Referer' : 'http://m.kugou.com/rank/info/8888',
        'Cookie' : 'UM_distinctid=161d629254c6fd-0b48b34076df63-6b1b1279-1fa400-161d629255b64c; kg_mid=cb9402e79b3c2b7d4fc13cbc85423190; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1523818922; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1523819865; Hm_lvt_c0eb0e71efad9184bda4158ff5385e91=1523819798; Hm_lpvt_c0eb0e71efad9184bda4158ff5385e91=1523820047; musicwo17=kugou'
        }

def get_songs(url):
    res=requests.get(url,headers=headers)
    return json.loads(res.text)

def get_song_download_url(url):
    res_tmp_list = get_songs(url)
    return res_tmp_list['data']['play_url']

def get_song_page_data(url):
    Song_Json = get_songs(url)
    Song_List_Json = Song_Json['data']['info']
    total = []
    for i in range(len(Song_List_Json)):
        song_download_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=%s&album_id=%s&_=1523819864065" % (Song_List_Json[i]['hash'], Song_List_Json[i]['album_id'])
        song_data_dict = {'downloadUrl':get_song_download_url(song_download_url),'fileName':Song_List_Json[i]['filename']}
        total.append(song_data_dict)
    return total

if __name__ == '__main__':
    keyword = raw_input("请输入歌名或者歌手:".decode('utf-8').encode('gbk'))
    if keyword:
        from urllib import quote
        import string
        keyword1 =  quote(keyword.decode('gbk').encode('utf8'), safe=string.printable)
        URL='http://mobilecdngz.kugou.com/api/v3/search/song?tag=1&tagtype=%E5%85%A8%E9%83%A8&area_code=1&plat=0&sver=5&api_ver=1&showtype=14&version=8969&keyword='+keyword1+'&correct=1&page=1&pagesize=10' #默认只取回10条记录 pagesize=10
        search_data = get_song_page_data(URL)
        for j in range(len(search_data)):
            print("%s   %s" % (search_data[j]['fileName'],search_data[j]['downloadUrl']))