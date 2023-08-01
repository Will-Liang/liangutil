# -*- coding: utf-8 -*-
import platform
import random
import time

import requests

from selenium.webdriver.chrome.options import Options

from selenium import webdriver

from liangutil.liangutils import print_log, get_nowdatetime

# 封装requests请求
class RequestUtils:

    def __init__(self, timeout:int, is_ssl_verify: bool, is_choice_agent:bool = True, proxies=None):
        self.timeout = timeout # 请求超时时间
        self.is_ssl_verify = is_ssl_verify # 是否验证SSL证书
        self.is_choice_agent = is_choice_agent # 是否随机AGENT
        # 该参数代理是为了需要用固定ip的爬虫
        self.proxies = proxies   # {'http': 'http://xxx', 'https': 'https://xxx'}

    def get_header(self,is_choice_agent=False):
        header = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept":"*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Accept-Encoding": "gzip, deflate",  # 使用gzip压缩传输数据让访问更快
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
            }
        if is_choice_agent == True:
            chrome_version = "Chrome/{}.0.{}.{}".format(random.randint(55, 82), random.randint(0, 4000),
                                                        random.randint(0, 150))
            os_type = ["(Windows NT 6.0; U; tr; rv:1.8.1)",
                       "(Windows NT 6.1; Win64; x64)"
                       "(Windows NT 6.1; WOW64)",
                       "(Windows NT 10.0; WOW64)",
                       "(X11; Linux x86_64)",
                       "(X11; Linux x86_64; rv:2.0b4)",
                       "(X11; U; FreeBSD x86_64; en-US)",
                       "(X11; Ubuntu; Linux x86_64; rv:24.0)"
                       "(Macintosh; Intel Mac OS X 10_12_6)",
                       "(Macintosh; U; Intel Mac OS X 10_12_6; en-us)",
                       "(Macintosh; U; Intel Mac OS X 10_12_6; ja-jp)",
                       ]
            browser_type = ["Mozilla/5.0",
                            ]
            ua = " ".join([random.choice(browser_type), random.choice(os_type), "AppleWebKit/537.36",
                           "(KHTML, like Gecko)", chrome_version, "Safari/537.36"])
            header["User-Agent"] = ua
        return header


    # Get 请求
    # 返回{
    #   "error": "", 错误信息
    #    "content": "",返回的内容
    #    "url": "" 请求的url
    # }
    def get(self, url, header="", retry_count=3, is_response_json=False, time_sleep=1, proxy=None):
        header = header if header else self.get_header(self.is_choice_agent)
        status_code = 200
        while retry_count > 0:
            retry_count = retry_count - 1
            try:
                if proxy == None and self.proxies == None:
                    resp = requests.get(url,headers=header, timeout=self.timeout, verify=self.is_ssl_verify)
                elif proxy != None:
                    resp = requests.get(url, headers=header, proxies=proxy,timeout=self.timeout, verify=self.is_ssl_verify)
                else:
                    resp = requests.get(url, headers=header, proxies=self.proxies, timeout=self.timeout,verify=self.is_ssl_verify)
                if resp.status_code == 200:
                    return {"error":"",
                            "content":resp.json() if is_response_json else resp.text,
                            "url":resp.url}
                else:
                    status_code = resp.status_code
                    time.sleep(time_sleep)


            except Exception as e:
                return {"error": e,
                        "content": "",
                        "url": url}

        return {"error": status_code,
                "content": "",
                "url": url}

    #  Post 请求
    # 返回{
    #   "error": "", 错误信息
    #    "content": "",返回的内容
    #    "url": "" 请求的url
    # }
    def post(self, method, url, header="", data=None, retry_count=3, is_response_json=False, time_sleep=1, proxy=None):
        header = header if header else self.get_header(self.is_choice_agent)
        status_code = 200
        while retry_count > 0:
            retry_count = retry_count - 1
            try:
                if proxy == None and self.proxies == None:
                    resp = requests.post(url,headers=header, data=data, timeout=self.timeout, verify=self.is_ssl_verify)
                elif proxy != None:
                    resp = requests.post(url, headers=header, data=data, proxies=proxy,timeout=self.timeout, verify=self.is_ssl_verify)
                else:
                    resp = requests.post(url, headers=header, data=data, proxies=self.proxies, timeout=self.timeout,verify=self.is_ssl_verify)
                if resp.status_code == 200:
                    return {"error":"",
                            "content":resp.json() if is_response_json else resp.text,
                            "url":resp.url}
                else:
                    status_code = resp.status_code
                    time.sleep(time_sleep)


            except Exception as e:
                return {"error": e,
                        "content": "",
                        "url": url}

        return {"error": status_code,
                "content": "",
                "url": url}


# https://selenium-python.readthedocs.io/page-objects.html
# https://www.selenium.dev/zh-cn/documentation/
# 封装 selenium
class ChromeUtils:
    def __init__(self, timeout: int, is_ssl_verify: bool=False, is_chrome_headless:bool = False, is_undetected_chromedriver:bool = False, proxy=None):
        self.timeout = timeout  # 请求超时时间
        self.is_ssl_verify = is_ssl_verify  # 是否验证SSL证书
        self.is_chrome_headless = is_chrome_headless # Linux下 is_chrome_headless为True
        self.is_undetected_chromedriver = is_undetected_chromedriver

        # 该参数代理是为了需要用固定ip的爬虫
        self.proxy = proxy # http://xxxxxx
        self.driver = self.get_chrome_driver(proxy)


    # 获得一个chrome驱动
    def get_chrome_driver(self, proxy=None):
        try:
            chrome_options = Options()

            if proxy != None:
                chrome_options.add_argument("--proxy-server="+proxy)
            elif self.proxy != None:
                chrome_options.add_argument("--proxy-server="+self.proxy)

            chrome_options.add_argument("-window-size=1920,1080") # 设置浏览器窗口的大小为1920x1080像素
            chrome_options.add_argument('--ignore-certificate-errors') # 忽略证书错误
            chrome_options.add_argument('--disable-gpu') # 禁用 GPU 硬件加速
            # chrome_options.add_argument('--incognito') #无痕模式 浏览器不会记录任何浏览历史或者cookie。

            # 禁止使用 /dev/shm。在某些系统中，Chrome 使用 /dev/shm 临时文件系统来共享数据，
            # 但在 Docker 或某些特定配置的系统中，这个文件系统可能会不够用，导致 Chrome 崩溃。
            # 这个选项可以让 Chrome 使用其它方式来共享数据，避免崩溃。
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--hide-scrollbars') # 隐藏滚动条
            chrome_options.add_argument('--disable-plugins') # 禁用插件
            # chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
            # 禁用沙箱。沙箱是 Chrome 用来隔离网页进程的一种安全机制，但在某些情况下，例如在 Docker 中运行 Chrome，沙箱可能会导致问题。这个选项可以禁用沙箱。
            chrome_options.add_argument('--no-sandbox')

            if self.is_chrome_headless:
                chrome_options.add_argument('--headless')
            if platform.system() == "Linux":
                chrome_options.add_argument('--headless')
                # 单进程模式。Chrome 默认会为每个标签页或插件启动一个新的进程，
                # 但在某些情况下，例如内存有限，可能希望所有的标签页都在一个进程中运行。这个选项可以让 Chrome 在单进程模式下运行。
                chrome_options.add_argument('--single-process')

            # undetected_chromedriver 是一个第三方库
            # 它可以规避某些网站对 selenium 的检测，使得你的自动化脚本更不容易被网站识别出来。
            # if self.is_undetected_chromedriver:
            #     import undetected_chromedriver as uc  # from session not created: This version of ChromeDriver only supports Chrome version 108
            #     driver = uc.Chrome(options=chrome_options)
            # else:
            #     driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.timeout) # 设置页面加载超时时间
            driver.set_script_timeout(self.timeout) # 设置脚本执行超时时间。

            return driver

        except Exception as e:
            return None

    # 重启浏览器
    def refresh_chrome(self):
        retry_time = 3
        time_sleep = 10
        error = ""
        while retry_time:
            try:
                if self.driver:
                    self.driver.quit()
                self.driver = self.get_chrome_driver()
                return True
            except Exception as e:
                retry_time = retry_time - 1
                error = str(e)
                time.sleep(time_sleep)
        print_log("ERROR", error)
        return False


    # 获得网页源码
    def get_page_source(self, url, time_sleep=0):
        print("{} Get {}".format(get_nowdatetime(), url))

        if self.driver == None:
            return {"error":"ZWChrome 的 driver 为空",
                    "content":"",
                    "url":url}
        try:
            self.driver.get(url)

        except Exception as e:
            if str(e).startswith("Message: timeout:") and self.driver.page_source:
                return {"error": "",
                        "content": self.driver.page_source,
                        "url": self.driver.current_url}

            if self.refresh_chrome():
                try:
                    self.driver.get(url)
                except Exception as e:
                    self.driver.execute("window.stop()")
                    return {"error":e,
                            "content":"",
                            "url":url}
            else:
                return {"error": "重启chrome失败","content": "","url": url}

        time.sleep(time_sleep)

        text = self.driver.page_source

        if text:
            return {"error": "",
                    "content": text,
                    "url": self.driver.current_url}
        else:
            return {"error": "没有获得 page_source",
                    "content": "",
                    "url": self.driver.current_url}



