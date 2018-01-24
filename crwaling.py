# 엑셀파일을 만들 모듈을 임포트 한다.
import xlsxwriter
# request 모듈을 임포트 한다.
import requests
# 파싱에 필요한 BeautifulSoup를 임포트 한다.
from bs4 import BeautifulSoup

# 페이지 정보를 가져오기 위한 get 요청
req = requests.get('http://www.jobkorea.co.kr/starter/?schPart=38888')
# HTML 소스 가져오기
html = req.text
# BeautifulSoup으로 html소스를 python객체로 변환하기
# 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
# 이 글에서는 Python 내장 html.parser를 이용했다.
soup = BeautifulSoup(html, 'html.parser')
# 페이지 정보를 가져온다.
page = soup.select(
    '.tplPagination > ul > li'
    )
# 기업명을 저장할 name
name = []
# 마감일자를 저장하기 위한 endday
endday = []
# 잡코리아는 페이지별로 받을수 있는 list가 정해져 있어서 page 별로 request를 보내야한다.
urlpage="http://www.jobkorea.co.kr/starter/?schPart=38888&Page="
# page 만큼 for문을 돈다.
for pa in page:
    sendpage=urlpage+str(pa.text)
    data = requests.get(sendpage)
    rawdata = data.text
    parser = BeautifulSoup(rawdata, 'html.parser')
    #리스트를 realdata 에 저장한후 그 값만큼 다시 for문을 돈다.
    realdata = parser.select(
    '.filterList li'
    )
    for q in realdata:
        # temp1값엔 기업명에 해당하는 값을 넣고
        temp1=q.select(
            '.co .coTit .coLink'
            )
        # temp2 값엔 마감일에 해당하는 값을 넣는다.
        temp2=q.select(
            '.side .day'
        )
        # 그리고 그 값을 각각 name 과 endday에 append를 해준다.
        name.append(temp1[0].string)
        endday.append(temp2[0].string)
# 마지막으로 name 과 endday에 해당하는 값을 엑셀에 저장.
print(name)
print(endday)

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('sample.xlsx')
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 20)

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

# Write some simple text.
worksheet.write('A1', '기업명')

# Text with formatting.
worksheet.write('B1', '마감일자')
number=0
for ind in name:
    # Write some numbers, with row/column notation.
    worksheet.write(number+1, 0, name[number])
    worksheet.write(number+1, 1, endday[number])
    number=number+1


workbook.close()
