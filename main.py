import requests
import os
import shutil

workpath = os.getcwd()

url = "http://103.204.13.68:8901/bbs/board.php?bo_table=toons&wr_id=757&stx=%EB%8F%84%EC%BF%84%EA%B5%AC%EC%9A%B8&is=7"
#url = input("URL: ")

r = requests.get(url)

html = r.text

temp = ""
title_pos = html.find('<meta property="og:title" content=') + 34 + 1
for j in range(title_pos, title_pos + 256):
    temp += html[j]
    if html[j] == '"':
        break

f = open(workpath + "\\" + "config.txt")
path = f.readline()
f.close()

title = temp[:-1]

path += "\\" + title
os.mkdir(path)
print(f"Title: {title}")
print(f"Path: {path}")

pos_img_list = html.find("img_list") + 11
temp = ""
img_list = []
for i in range(pos_img_list, pos_img_list + 9999999):
    temp += html[i]
    if html[i] == ']':
        break

img_list = temp[2:-2].split('","')

print(f"Images: {len(img_list)}")

img_path = path + "\\" + title + "_"
img_count = len(img_list)

for i in range(img_count):
    curr_img_path = img_path + str(i+1) + ".jpeg"
    r = requests.get(img_list[i], stream=True)
    if r.status_code == 200:
        with open(curr_img_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        print(f"Downloaded {i+1}/{img_count} ({(i+1)/img_count*100}%)")
    else:
        print(r.status_code)
        exit(0)
