import requests
from bs4 import BeautifulSoup
import re
import telepot
import time

#---------------------
num = 0
mlist = ['정보보안', '관제', '전산', '포렌식', '취약점']
POST = {
	'flag':'U',
	'empmnsn' : '',
	'searchJobsecode' : '020'
}

#---------------텔레그램 설정부분----------#
sbot = telepot.Bot('573040620:AAE5B4uWaDNltEN0LgxRJ2kX3DaJ_souT0k')
sbot.getMe()
#-----------------------------------------#


# 최신 글번호 조회 함수 ---------------------------------------------------------------
def checkNum() :
	s = requests.get('https://www.gojobs.go.kr/apmList.do?menuNo=6&empmnsn=0&searchJobsecode=&searchBbssecode=0&searchBbssn=0',verify=False).text
	soup = BeautifulSoup(s, 'html.parser')
	t2 = soup.select('a')
	m = re.compile('[0-9]{5,6}').search(str(t2[0]))
	return(int(m.group(0)))
#-----------------------------------------------------------------------------------

# 글 내용 확인 함수 -----------------------------------------------------------------
def checkContent() :
	s = requests.post('https://www.gojobs.go.kr/apmView.do', data=POST, verify=False).text
	soup = BeautifulSoup(s, 'html.parser')
	t2 = soup.select('table')
	for i in mlist :
		if re.search(i,str(t2)) != None :
			sbot.sendMessage(-1001151947775,soup.select('p.title')[0].text+' / '+soup.select('td')[1].text+'\n https://www.gojobs.go.kr/frameMenu.do?url=apmList.do&menuNo=6')
#-----------------------------------------------------------------------------------
            


num = checkNum()
POST['empmnsn'] = num
    
while(True):
	try:
		if num < checkNum():
			num += 1
			POST['empmnsn'] = num
			checkContent()
			time.sleep(300)
	except:
		print('error.. why..?')
		time.sleep(300)
