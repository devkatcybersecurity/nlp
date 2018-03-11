import os
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import requests
from doc_text import get_docx_text 

# url = 'https://hudoc.echr.coe.int/app/conversion/docx/?library=ECHR&id=001-181202&filename=CASE%20OF%20MOCKUT%u0116%20v.%20LITHUANIA.docx'
# output = 'data.docx'

# urllib.request.urlretrieve(url, output)

# url2 = 'https://hudoc.echr.coe.int/eng#{%22languageisocode%22:[%22ENG%22],%22documentcollectionid2%22:[%22CHAMBER%22],%22violation%22:[%226%22]'

# data = requests.get(url2)
# print(data.text)
# data = urllib.request.urlopen(url2)

http_proxy = "http://devk:dev34195@nknproxy.iitk.ac.in:3128/"
https_proxy = "https://devk:dev34195@nknproxy.iitk.ac.in:3128/"
ftp_proxy = "ftp://devk:dev34195@nknproxy.iitk.ac.in:3128/"
proxyDict = {
            "http":http_proxy,
            "https":https_proxy,
            "ftp":ftp_proxy
            }

article = 'nv3.html'
data = open('pro/%s'%(article),'r',encoding='ISO-8859-1')
data = data.read()
# data = data.decode('utf-8')
soup = BeautifulSoup(data,'html.parser')
dir1 = './temp/'+str(article[:-5])
dir2 = './data/'+str(article[:-5])
if not os.path.exists(dir1):
    os.makedirs(dir1)
if not os.path.exists(dir2):
    os.makedirs(dir2)

count = 1
for links in soup.find_all("a",{"class":"document-link headline"}):
    if(links['href'][30:36]=='itemid' and links['href'][1:4]=='eng'):
        url = 'https://hudoc.echr.coe.int/app/conversion/docx/?'
        filename = links.text+'.docx'
        id_str=links['href'][40:-3]
        print(filename)
        param = urllib.parse.urlencode({'library':'ECHR','id':id_str,'filename':filename})
        r = requests.get(url+param,proxies=proxyDict)
        print(r.status_code)
        if(r.status_code==200):
            urllib.request.urlretrieve(url+param,str(dir1+"/"+str(count)+".docx"))
            with open(str(dir2+"/"+(str(count)+'.txt')),'w') as f:
                f.write(get_docx_text(str(dir1+"/"+(str(count)+'.docx'))))
            print(count)
            count +=1
    else:
        print('false')
        print(links['href'])

print("total counts are ", count-1)

