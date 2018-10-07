#調試文件
from scrapy.cmdline import execute

import sys
import os
#獲取當前文件的父目錄
#print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","jobbole"])