import hashlib

def get_md5(url):
    # 判斷傳過來的路徑是不是unicode是的話就進行utf-8
    if isinstance(url,str):
        url = url.encode("utf8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print(get_md5("http://jobbole.com/".encode("utf8")))
