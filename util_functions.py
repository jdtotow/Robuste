
"""Traitement nom de domaine"""
import re
import sys
import urllib2
################################################ 
liste_domain=[]
#################################################

class WordList :
    def __init__(self,domain):
        self.list = []
        self.domain = domain
    def add(self,word):
        if not word in self.list:
            self.list.append(word)
    def addList(self,liste):
        for l in liste:
            self.add(l)
    def save(self):
        #letter = self.domain.split(".")[1]
        fichier = open('wordlist_essai','a')
        for w in self.list :
            fichier.write(w+'\n')
        fichier.close()
    def size(self):
        return len(self.list)   
    def getList(self):
        return self.list
    def getDomainName(self):
        return self.domain

#################################################

class SmartList :
    def __init__(self):
        self.my_list=[]
        self.size = 0
        
    def add(self,domain):
        if not domain in self.my_list:
            self.my_list.append(domain)
            self.size=self.size+1
        if self.size == 10:
            self.save()
            self.my_list.clear()
            self.size=0
                
    def save(self):
        fichier = open('domain.txt','a')
        for domain in self.my_list:
            fichier.write(domain+'\n')
        fichier.close()
        
################################################               
    
class MainList :
    def __init__(self):
        self.my_list=[]
        self.size = 0
        self.max = 500
    def loadFile(self):
        fichier = open('domain.txt','a')
        content = fichier.read()
        global liste_domain
        liste_domain = content.split('\n')
        fichier.close()
    def add(self,element):
        if self.size >= self.max:
            return 
        if not element in self.my_list :
            self.my_list.append(element)
            self.size=self.size + 1
    def pop(self):
        if self.size > 0 :
            self.size = self.size - 1
            return self.my_list.pop(0)
            
###############################################
            
class Link:
    def __init__(self,domain):
        self.domain= domain
        self.link = ""
    def addLink(self,link):
        self.link = link
    def getLink(self):
        return self.link
        
################################################
       
class Domain: 
    def __init__(self):
        self.name =""
        self.links = []
        self.links_done = []
    def addName(self,domain):
        self.name = domain
        self.wordList = WordList(self.name)
    def addLink(self,link):
        if self.name=="":
            return
        for l in self.links:
            if l.getLink()==link:
                print("lien existant")
                return
        for l in self.links_done:
            if l.getLink() == link:
                print("lien deja scanne")
                return
        l=Link(self.name)
        l.addLink(link)
        global liste_domain
        if self.name in link:
            self.links.append(l)
            print("lien ajoute "+str(len(self.links)))
        else:
            liste_domain.append(result)
            
    def addLinkList(self,liens):
        for l in liens:
            self.addLink(l)
            
    def scan(self):
        while len(self.links)!=0:
            lien = self.links.pop(0)
            try:
                content = urllib2.urlopen(lien.getLink()).read()
                liens_found = find_url(self.name,content)
                self.addLinkList(liens_found)
                words = find_word(content)
                self.wordList.addList(words)
                print("Lien scannee : "+lien.getLink())
                self.links_done.append(lien)
            except:
                print(lien.getLink()+", Liens morts")
                
        self.wordList.save()
                                      
    def addWord(self,word):
        self.wordList.add(word) 
                     
    def nbLink(self):
        return len(self.links)
        
    def getLinks(self):
        return self.links  
    def getName(self):
        return self.name 
              
#####################################################     
def find_www_domain(name_domain):
    if name_domain=="":
        print("Erreur nom de domaine ")
    regexp=r"[A-Za-z-0-9]+"
    result=re.findall(regexp,name_domain)
    if len(result)==1:
        return result[0]
    if len(result)==3 and result[0]=="www":
        return name_domain
    else:
        return "http://www."+result[-2]+"."+result[-1]
######################################################

"""       
t=["www.efi.cd","42.fr","der.www.france24.fr","23.fr.google.com"]
for i in t:
    print find_www_domain(i)
"""
#domain="www.robuste.com"
#content=html code
  
def find_word(content):
    result = []
    regexp=r'>.*?<'
    liste = re.findall(regexp,content)
    for l in liste:
        chaine=l[1:-1]
        t = chaine.split(" ")
        result=result+t
        
    return list(set(result))
    
def find_url(domain,content):
    if domain[-1]=="/":
        domain=domain[:-1]
    list_url=[]
    regexp=r'<a.*?href=["\']*(.+?)["\'>]'
    list_href = re.findall(regexp,content,flags=re.I)
    #print list_href
    for url in list_href:
        if "mailto:" in url or url=="#":
            continue                
        if "www." in url or "http://" in url or "https://" in url or domain in url:
            list_url.append(url)
        else:
            if url[0]=="/":
                list_url.append(domain+url)
            else:
                list_url.append(domain+"/"+url[0:])
                
    return list_url
        

def save_error(e):
    fichier = open('domain_error.txt','a')
    fichier.write(e+'\n')  
    fichier.close()
    
"""
fichier = open("sommaire.htm","r")
content = fichier.read()
f = open('urls.txt','a')
for url in find_url("sametmax.com",content):
    f.write(url+'\n')
f.close()
"""
d = Domain()
d.addName("http://localhost/whosgotthegroove")
d.addLink("http://localhost/whosgotthegroove/index.php")
d.scan()
