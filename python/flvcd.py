#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2


class Flcvd():
    url_head = "http://www.flvcd.com/parse.php?"
    url_tail = "&flag=one&format=high"
    pat_urls = re.compile(r'name="inf" value="(.*?)"')

    def __init__(self, url):
        self.src_url = url

    def parse(self):
        # url
        url_kw = urllib.urlencode({'kw' : self.src_url})
        flvcd_url = self.url_head + url_kw + self.url_tail

        # headers
        flvcd_headers = {
            'Host' : 'www.flvcd.com',
            'Referer' : flvcd_url,
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97'
        }

        # request - response
        req = urllib2.Request(url = flvcd_url, headers = flvcd_headers)
        resp = urllib2.urlopen(req)
        content = resp.read()
# <input type="hidden" name="inf" value="http://vod.cntv.lxdns.com/flash/mp4video50/TMS/2016/03/28/5b14b9230e3b4af2ad1f340cb80f1608_h264818000nero_aac32-1.mp4|http://vod.cntv.lxdns.com/flash/mp4video50/TMS/2016/03/28/5b14b9230e3b4af2ad1f340cb80f1608_h264818000nero_aac32-2.mp4|http://vod.cntv.lxdns.com/flash/mp4video50/TMS/2016/03/28/5b14b9230e3b4af2ad1f340cb80f1608_h264818000nero_aac32-3.mp4|http://vod.cntv.lxdns.com/flash/mp4video50/TMS/2016/03/28/5b14b9230e3b4af2ad1f340cb80f1608_h264818000nero_aac32-4.mp4|"/>
        url_found = self.pat_urls.findall(content)
        if not url_found:
            return None
        url_list = url_found[0].split('|')
        for url in url_list:
            if not url:
                continue
            print url


if __name__ == '__main__':
    url = "http://tv.cctv.com/2016/03/28/VIDErJCd2VVkgDiVer9EuaRT160328.shtml"
    flcvd = Flcvd(url)
    flcvd.parse()


