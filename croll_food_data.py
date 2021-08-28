from selenium import webdriver
import re
import time
import pickle

Start = 90001 #시작,끝페이지 설정~$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
End = 93000 #로딩이 다된다음 페이지를 바꿔준다 

driver = webdriver.Chrome(r"C:\\chromedriver.exe")#경로지정~$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
url = "http://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoProduct.do?menu_grp=MENU_NEW04&menu_no=2815#page1"
driver.get(url)
driver.find_element_by_id('srchBtn').click()

sickpoom_dic = {}
ruaz = Start
while ruaz < End:
    ex_ruaz = ruaz
    try:
        time.sleep(2)
        html = driver.page_source  # 페이지의 elements모두 가져오기
        #soup = BeautifulSoup(html, 'html.parser')
        table = driver.find_element_by_id('tbl_prd_list')
        tbody = table.find_element_by_tag_name("tbody")
        rows = tbody.find_elements_by_tag_name("tr")
        page_num = int(driver.find_element_by_id(
            "s_page_num").get_attribute("value"))
        # print(page_num)
        for index, value in enumerate(rows):
            product_shelf_life = value.find_elements_by_tag_name("td")[4]
            product_name = value.find_elements_by_tag_name("td")[5]
            sickpoom_dic[product_name.text] = product_shelf_life.text
            # print(product_name.text, product_shelf_life.text)
            # print(ruaz, len(sickpoom_dic))
        if ruaz == page_num:
            if(ruaz <= 3 or ruaz >= 135979):
                driver.find_element_by_xpath(
                    '//*[@id="contents"]/div[3]/div/ul/li[10]/a').click()
            elif(ruaz == 4 or ruaz == 135978):
                driver.find_element_by_xpath(
                    '//*[@id="contents"]/div[3]/div/ul/li[11]/a').click()
            elif(ruaz == 5 or ruaz == 135977):
                driver.find_element_by_xpath(
                    '//*[@id="contents"]/div[3]/div/ul/li[12]/a').click()
            elif(ruaz >= 6 or ruaz >= 135976):
                driver.find_element_by_xpath(
                    '//*[@id="contents"]/div[3]/div/ul/li[13]/a').click()
            driver.implicitly_wait(60)
            ruaz += 1
        else:
            ruaz -= 1
    except:
        ruaz = ex_ruaz
        print('excpet')

regex0 = re.compile(r'\d+개월')
regex0_0 = re.compile(r'\d+ 개월')
regex1 = re.compile(r'\d+시')
regex1_0 = re.compile(r'\d+ 시')
regex2 = re.compile(r'\d+년')
regex2_0 = re.compile(r'\d+ 년')
regex3 = re.compile(r'\d+일')
regex3_0 = re.compile(r'\d+ 일')

regex = []
regex.append(regex0)
regex.append(regex0_0)
regex.append(regex1)
regex.append(regex1_0)
regex.append(regex2)
regex.append(regex2_0)
regex.append(regex3)
regex.append(regex3_0)

keyList = sickpoom_dic.keys()  # 키 리스트 뽑기
number_dict = {}
bul = False
for key in keyList:
  for i in regex:
    if i.search(sickpoom_dic[key]) != None:
      matchobj = i.search(sickpoom_dic[key])
      number_dict[key] = matchobj.group()
      bul = True
  if bul != True:
    number_dict[key] = "null"
    bul = False

with open('90001~93000.pkl', 'wb') as f: #저장할때 이름 바꿔주세요~$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    pickle.dump(number_dict, f)

# with open('data_dict.pkl', 'rb') as f:
#     mydict = pickle.load(f)

# print(mydict)
