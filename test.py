#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import hashlib
import cStringIO
from PIL import Image
import captcha
import re
import sys
import xlwt
from prettytable import PrettyTable
reload(sys)
sys.setdefaultencoding('utf-8')

print u'WHU成绩查询 免验证码ver 0.1\ntofu\n'
print u'输入学号：'
id = raw_input()
print u'输入密码：'
pwdinput = raw_input()
pwd = hashlib.md5()
pwd.update(pwdinput)
header = {'useragent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
captchaurl = 'http://210.42.121.241//servlet/GenImg'
loginurl = 'http://210.42.121.241/servlet/Login'
scoreurl = 'http://210.42.121.241/stu/stu_score_parent.jsp'
sys.setrecursionlimit(10000)

#登陆并获取登陆成功cookie
while 1:
	cap = requests.get(captchaurl)
	Ccookies = cap.cookies
	tmpIm = cStringIO.StringIO(cap.content)
	capim = Image.open(tmpIm)
	bin_im = captcha.binarize_image(capim)
	bin_cl_im = captcha.clearnoise(bin_im, 3, 1)
	yzm = captcha.image_to_text(bin_cl_im)
	params = {'id':id, 'pwd':pwd.hexdigest(),'xdvfb':yzm}
	homepage_session = requests.session()
	homepage = homepage_session.post(loginurl, headers = header, params = params, cookies = Ccookies)

	bs = BeautifulSoup(homepage.text, 'lxml')
	alert = bs.body.find_all(id = 'alertp')
	if alert:
		pass
	else:
		print u'登陆成功！'
		break

#武大教务系统登陆成功不返回新cookie，而是继续使用验证码cookie
scorepage = requests.get(scoreurl, headers= header, cookies= Ccookies)
bs_s = BeautifulSoup(scorepage.text, 'lxml')
pattern = re.compile('csrftoken=(.*?)&year', re.S)
token = re.findall(pattern, str(bs_s.head))

score_result_url = 'http://210.42.121.241/servlet/Svlt_QueryStuScore?csrftoken=' + token[0] + '&year=0&term=&learnType=&scoreFlag=0&t=0'

score_result_page = requests.get(score_result_url, headers= header, cookies= Ccookies)
bs_score = BeautifulSoup(score_result_page.text, 'lxml')



score_list = bs_score.find_all('td')
score_list_str = []
for item in score_list:
	score_list_str.append(item.string)


index = 0
subject_score = []
num = len(score_list_str) / 11
for i in range(0, num):
	subject_score.append(score_list_str[i * 11 : i * 11 + 10])

# table = PrettyTable([u'课程',u'类别',u'学分',u'分数'])
# table.align[u'课程'] = 'l'
# table.padding_width = 1
#
# for item in subject_score:
# 	try:
# 		#table.add_row(['1', '1', '1', '1'])
# 		print item[1].decode('utf-8')+'   '+item[2].decode('utf-8')
# 		table.add_row([item[1].encode('utf-8'),item[2].encode('utf-8'),item[3].encode('utf-8'),item[9].encode('utf-8')])
# 	except AttributeError:
# 		continue
# print table

workbook = xlwt.Workbook()
sheet = workbook.add_sheet(u'成绩',cell_overwrite_ok=True)
style = xlwt.easyxf('font: bold 1')
sheet.write(0,0,u'科目',style)
sheet.write(0,1,u'类别',style)
sheet.write(0,2,u'学分',style)
sheet.write(0,3,u'分数',style)
count = 1
for item in subject_score:
	sheet.write(count, 0, item[1])
	sheet.write(count, 1, item[2])
	sheet.write(count, 2, item[3])
	sheet.write(count, 3, item[9])
	count += 1
sheet.col(0).width = 256*26
workbook.save('report.xls')
print u"成绩已生成于report.xls\n任意键退出..."
e = raw_input()