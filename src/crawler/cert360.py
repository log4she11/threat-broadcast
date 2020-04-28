#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/4/25 22:17
# @File   : cert360.py
# -----------------------------------------------
# 360：https://cert.360.cn/warning
# -----------------------------------------------

from src.bean.cve_info import CVEInfo
from src.crawler._base_crawler import BaseCrawler
from src.utils import log
import requests
import json
import re
import time


class Cert360(BaseCrawler):

    def __init__(self):
        BaseCrawler.__init__(self)
        self.soure = '奇虎 360'
        self.url_list = 'https://cert.360.cn/warning/searchbypage'
        self.url_cve = 'https://cert.360.cn/warning/detail?id='



    def cve_news(self):
        old_cves = []
        try:
            new_cves = self.get_cves()
        except:
            log.error('获取 [%s] 威胁情报异常' % self.soure)


    def get_cves(self, limit = 6):
        params = {
            'length': limit,
            'start' : 0
        }

        response = requests.get(
            self.url_list,
            headers = self.headers(),
            params = params,
            timeout = self.timeout
        )

        cves = []
        if response.status_code == 200:
            json_obj = json.loads(response.text)
            for obj in json_obj.get('data'):
                cve = self.to_cve(obj)
                if cve.is_vaild():
                    cves.append(cve)
                    log.debug(cve)
        else:
            log.warn('获取 [%s] 威胁情报失败： [HTTP Error %i]' % (self.soure, response.status_code))
        return cves


    def to_cve(self, json_obj):
        cve = CVEInfo()
        cve.src = self.soure
        cve.url = self.url_cve + (json_obj.get('id') or '')
        cve.info = (json_obj.get('description') or '').strip().replace('\n\n', '\n')

        seconds = json_obj.get('add_time') or 0
        localtime = time.localtime(seconds)
        cve.time = time.strftime('%Y-%m-%d %H:%M:%S', localtime)

        title = json_obj.get('title') or ''
        cve.title =  re.sub(r'CVE-\d+-\d+:', '', title).strip()

        rst = re.findall(r'(CVE-\d+-\d+)', title)
        cve.id = rst[0] if rst else ''
        return cve



