# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 16:00
# @Author  : Dd
# @File    : search_t6ss.py

import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import time
import random

# 定义请求头
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'Accept-encoding': 'gzip, deflate, br',
           'Accept-language': 'zh-CN,zh;q=0.9',
           'Host': 'www.ncbi.nlm.nih.gov',
           'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
# 获取cookie
cookies = requests.get('https://www.ncbi.nlm.nih.gov/protein/?term=Type+VI+secretion+system', headers=headers).cookies
proxies = {'http':'http://171.39.6.204:8123', 'https':'https://125.126.216.160:9999'}
# 保存accession,GI信息
accessions = []
GI = []


# 解析检索页面
def get_acc_info(url):
    accession = []
    # 准备post获取返回信息
    data = {'term': 'Type VI secretion system',
            'EntrezSystem2.PEntrez.Protein.Sequence_PageController.PreviousPageName': 'results',
            'EntrezSystem2.PEntrez.Protein.Sequence_Facets.FacetsUrlFrag': 'filters=',
            'EntrezSystem2.PEntrez.Protein.Sequence_Facets.FacetSubmitted': 'false',
            'EntrezSystem2.PEntrez.Protein.Sequence_Facets.BMFacets':'',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.sPresentation': 'docsum',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.sPageSize': '20',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.sSort': 'none',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.FFormat': 'docsum',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.FSort': '',
            'coll_start': 1,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.Db': 'protein',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.QueryKey': 1,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.CurrFilter': 'all',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.ResultCount': 1183522,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.ViewerParams': '',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.FileFormat': 'docsum',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.LastPresentation': 'docsum',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.Presentation': 'docsum',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.PageSize': 20,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.LastPageSize': 20,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.Sort': '',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.LastSort': '',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.FileSort': '',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.Format': '',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.LastFormat': '',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.PrevPageSize': 20,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.PrevPresentation': 'docsum',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.PrevSort': '',
            'CollectionStartIndex': 1,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_ResultsController.ResultCount': 1183522,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_ResultsController.RunLastQuery': '',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_ResultsController.AccnsFromResult': '',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Entrez_Pager.cPage': 1,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Entrez_Pager.CurrPage': 1,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Entrez_Pager.cPage': 1,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.sPresentation2': 'docsum',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.sPageSize2': 20,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.sSort2': 'none',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.FFormat2': 'docsum',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.FSort2': '',
            'coll_start2': 1,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_MultiItemSupl.Taxport.TxView': 'list',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_MultiItemSupl.Taxport.TxListSize': 5,
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_MultiItemSupl.RelatedDataLinks.rdDatabase': 'rddbto',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_MultiItemSupl.RelatedDataLinks.DbName': 'protein',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Discovery_SearchDetails.SearchDetailsTerm': 'Type VI secretion system[Protein Name] OR (Type[All Fields] AND VI[All Fields] AND secretion[All Fields] AND system[All Fields])',
            'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.HistoryDisplay.Cmd': 'PageChanged',
            'EntrezSystem2.PEntrez.DbConnector.Db': 'protein',
            'EntrezSystem2.PEntrez.DbConnector.LastDb': 'protein',
            'EntrezSystem2.PEntrez.DbConnector.Term': 'Type VI secretion system',
            'EntrezSystem2.PEntrez.DbConnector.LastTabCmd': '',
            'EntrezSystem2.PEntrez.DbConnector.LastQueryKey': 1,
            'EntrezSystem2.PEntrez.DbConnector.IdsFromResult': '',
            'EntrezSystem2.PEntrez.DbConnector.LastIdsFromResult': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkName': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkReadableName': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkSrcDb': '',
            'EntrezSystem2.PEntrez.DbConnector.Cmd': 'PageChanged',
            'EntrezSystem2.PEntrez.DbConnector.TabCmd': '',
            'EntrezSystem2.PEntrez.DbConnector.QueryKey': '',
            'p$a': 'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Entrez_Pager.Page',
            'p$l': 'EntrezSystem2',
            'p$st': 'protein'}
    while(1):
        try:
            for i in range(1, 59491):
                data['EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Entrez_Pager.CurrPage'] = i
                data['EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.HistoryDisplay.Cmd'] = 'PageChanged'
                data['EntrezSystem2.PEntrez.DbConnector.Cmd'] = 'PageChanged'
                data['coll_start'] = 20*i+1
                data['coll_start2'] = 20*i+1
                data['p$a'] = 'EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Entrez_Pager.Page'
                data['p$l'] = 'EntrezSystem2'
                data['p$st'] = 'protein'
                data['CollectionStartIndex'] = 1
                r = requests.post(url, data=data, cookies=cookies, headers=headers)
                soup = BeautifulSoup(r.content, features="lxml")
                dd = soup.find_all(name='dd')
                for k in dd:
                    p = str(k)
                    if re.findall('<dd>([a-zA-Z]{3}.*)</dd>', p, re.S):
                        accession.append(p)
                    if re.findall('>*\d<', p):
                        c = re.findall('>\d*<', p)
                        if c not in GI:
                            GI.append(c)
                time.sleep(random.randint(0, 2))
                print('accession_page_percent: {:.2%}'.format(i / 59491))
            for j in accession:
                if re.findall('[a-zA-Z]{3}.*\d', j):
                    a = re.findall('[a-zA-Z]{3}.*\d', j)
                    if a not in accessions:
                        accessions.append(a)
            GI.pop(0)
            return accessions, GI
        except:
            print('bad')
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            continue


# 创建字典，用列表存储序列相关信息：title, organisms, journal, fasta
info = defaultdict(dict)


# Ajax 提取
def get_seq_info(accessions, GI, i):
    """
    :param accessions:
    :return: organisms, sequence, organisms, .fasta file
    """
    baseurl = 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?'
    base_url = 'https://www.ncbi.nlm.nih.gov/protein/'
    for acc in accessions[i]:
        for G in GI[i]:
            accession = str(acc).replace("['", '').replace("']", '')
            gi = str(G).replace("['>", '').replace("<']", '').strip('>').strip('<')
            params = {'id': gi,
                      'db': 'protein',
                      'report': 'genpept',
                      'conwithfeat': 'on',
                      'show-cdd': 'on',
                      'retmode': 'html',
                      'withmarkup': 'on',
                      'tool': 'portal',
                      'log$': 'seqview',
                      'maxdownloadsize': 1000000}
            params['id'] = gi
            acc_url =baseurl + 'id='+gi+'&db=protein&report=genpept&conwithfeat=on&show-cdd=on&retmode=html&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000'
            fasta_url = baseurl + 'id='+gi+'&db=protein&report=fasta&extrafeat=null&conwithfeat=on&retmode=html&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000'
            while(1):
                try:
                    # 解析accession 页面
                    doc = requests.get(acc_url, headers=headers, cookies=cookies)
                    if doc.status_code == 200:
                        gene = re.findall('/gene="\w*?A.*?"\n', doc.text)
                        if gene:
                            # 获取title
                            soup = BeautifulSoup(requests.get(base_url + accession, headers=headers, cookies=cookies).content, 'lxml')
                            title = soup.title.string.replace(' - Protein - NCBI', '').strip("['").strip("']")
                            info[str(accessions[i]).replace('[\'', '').replace('\']', '')]['title'] = title
                            # 获取fasta
                            fasta = requests.get(fasta_url, headers=headers, cookies=cookies).text
                            info[str(accessions[i]).replace('[\'', '').replace('\']', '')]['fasta'] = fasta.replace('\n', '')
                            print('info_percent: {:.2%}'.format(i / 1189785))
                        return doc.text, info
                except requests.ConnectionError as e:
                    print('Error', e.args)
                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    continue


def main():
    url = 'https://www.ncbi.nlm.nih.gov/protein/?term=Type+VI+secretion+system'
    # 保存到本地，输出格式：'accessions\ttitle\tfasta'
    # 用字典的方法来获取键的值
    for i in range(1189785):
        get_acc_info(url)
        get_seq_info(accessions, GI, i)
        time.sleep(random.randint(0, 2))


main()

wd = 'D:\\Postgraduate\\spider_data\\info.txt'
with open(wd, 'a+', encoding='utf-8') as file:
    for k, v in info.items():
        file.write(v['fasta']+'\n')
