import requests
import os
import shutil
import bs4 as bs

workpath = os.getcwd()

url = "http://103.204.13.68:8901/bbs/board.php?bo_table=toons&stx=%EB%8F%84%EC%BF%84%EA%B5%AC%EC%9A%B8&is=7&sord=&type=&page=2"
#url = input("Download from (input URL): ")
r = requests.get(url)
html = r.text

url_cut = url[:url.find("board")-1]
url_list = []

soup = bs.BeautifulSoup(html, 'html.parser')
for li in soup.find_all('li'):
    #print(li)   location.href='.
    if len(li.findChildren("button")) != 0 and len(li.findChildren("input")) != 0:
        url_list.append(url_cut + str(li.findChildren("button", recursive=False)[0]["onclick"])[16:-1])

#print(url_list)

url_count = len(url_list)

for k in range(url_count):
    url = url_list[k]

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
    title = title.replace(":", "")
    path += "\\" + title
    try:
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

        print("Done!")
    except Exception as ex:
        print(ex)
