import openpyxl
import re

with open('Data\\access.2023-08-19.log', 'r') as file:
    content = file.read()

lines = content.split('\n')

counter = {}
for line in lines[:-1]:
    cells = line.split(' ')

    date = cells[3][1:cells[3].find(':')]

    time = cells[3][13:21]
    time_index = time.find(':')
    time = int(time[:time_index])

    url = "root" if not cells[6][0:] else cells[6][0:].partition('?')[0]
    url = re.sub(r'/\d+', '', url)

    if (".js" in url) or (".css" in url) or (".ico" in url) or (".png" in url) or (".webp" in url) or (".svg" in url) or ("Wx" in url) or (".jpg" in url) or (".woff2" in url) or (".ttf" in url) or (".woff" in url):
        pass
    else:
        if date in counter:
            if url in counter[date]:
                if time in counter[date][url]:
                    counter[date][url][time] += 1
                else:
                    counter[date][url][time] = 1
            else:
                counter[date][url] = {time:  1}
        else:
            counter[date] = {url: {time:  1}}
workbook = openpyxl.Workbook()


sheet = workbook.active

sheet['A1'] = "Operation"
sheet['B1'] = "Operation_count"
sheet['C1'] = "Date"
sheet['D1'] = "Hour"

row_num = 2
for date, value in counter.items():
    for url, value1 in value.items():
        for time, count in value1.items():
            sheet.cell(row=row_num, column=1).value = url
            sheet.cell(row=row_num, column=2).value = count
            sheet.cell(row=row_num, column=3).value = date
            sheet.cell(row=row_num, column=4).value = time
            row_num += 1

workbook.save('Result\\outputTest1.xlsx')