# -*- coding: utf-8 -*-
import os
import platform
import random
import time
import requests
import wget
import shutil


from func_timeout import func_set_timeout, FunctionTimedOut
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from liangutil.liangutils import *

"""
requestutils 中封装了爬虫的类以及方法
"""

# 封装requests请求
class RequestUtils:
    """
    RequestUtils 基于 requests 库进行的封装
    """

    def __init__(self, timeout:int, is_ssl_verify: bool, is_choice_agent:bool = True, proxies=None, proxy_host=None):
        """
        初始化 RequestUtils

        Args:
            timeout(int): 请求超时时间
            is_ssl_verify(bool): 是否验证 SSL 证书
            is_choice_agent(bool): 是否随机 USER-AGENT
            proxies(dict): 代理字典
            proxy_host(str): 代理
        """
        self.timeout = timeout # 请求超时时间
        self.is_ssl_verify = is_ssl_verify # 是否验证SSL证书
        self.is_choice_agent = is_choice_agent # 是否随机AGENT

        # 该参数代理是为了需要用固定ip的爬虫
        self.proxies = proxies   # {'http': 'http://xxx', 'https': 'https://xxx'}

        self.proxy_host = (proxy_host if "://" in proxy_host else "socks5://" + proxy_host) if proxy_host and isinstance(proxy_host,str) else None

    def get_header(self,is_choice_agent=False):
        """获得 USER-AGENT

        Args:
            is_choice_agent(bool): 是否随机 USER-AGENT

        Returns:
            str: USER-AGENT

        """
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


    def get(self, url, headers="", retry_count=3, is_response_json=False, time_sleep=1, proxies=None):
        """Get 请求

        Args:
            url(str): 请求的url
            headers(str): 请求头
            retry_count(int): 重试次数
            is_response_json(bool): 返回的是否是json
            time_sleep(int): 请求失败后的停止时间
            proxies(dict): 代理

        Returns:
            dict: {"error": "状态码/异常", "content": "网页源码/json","url": "请求的url"}

        """
        header = headers if headers else self.get_header(self.is_choice_agent)
        status_code = 200
        while retry_count > 0:
            retry_count = retry_count - 1
            try:
                if proxies == None and self.proxies == None:
                    resp = requests.get(url,headers=header, timeout=self.timeout, verify=self.is_ssl_verify)
                elif proxies != None:
                    resp = requests.get(url, headers=header, proxies=proxies,timeout=self.timeout, verify=self.is_ssl_verify)
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


    def post(self, url, headers="", data=None, retry_count=3, is_response_json=False, time_sleep=1, proxies=None):
        """Post 请求

        Args:
            url(str): 请求的url
            headers(str): 请求头
            data(dict): payload
            retry_count(int): 重试次数
            is_response_json(bool): 返回的是否是json
            time_sleep(int): 请求失败后的停止时间
            proxies(dict): 代理

        Returns:
            dict: {"error": "状态码/异常", "content": "网页源码/json","url": "请求的url"}

        """
        header = headers if headers else self.get_header(self.is_choice_agent)
        status_code = 200
        while retry_count > 0:
            retry_count = retry_count - 1
            try:
                if proxies == None and self.proxies == None:
                    resp = requests.post(url,headers=header, data=data, timeout=self.timeout, verify=self.is_ssl_verify)
                elif proxies != None:
                    resp = requests.post(url, headers=header, data=data, proxies=proxies,timeout=self.timeout, verify=self.is_ssl_verify)
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


    def file_download_once(self, url, file=""):
        """从指定URL下载单个文件的方法

        Args:
            url(str): url
            file(str): 文件名

        Returns:
            True/False
        """
        if file:
            wget.download(url, file)
            return True
        else:
            if self.proxies:
                return requests.get(url, headers=self.get_header(), proxies=self.proxies, stream=True,
                                    timeout=self.timeout)  # stream=True
            else:
                return requests.get(url, headers=self.get_header(), stream=True, timeout=self.timeout)  # stream=True


    def file_download_github(self, github_author, github_project, file_path):
        """下载代码仓库

        Args:
            github_author(str):项目作者
            github_project(str):项目名称
            file_path(str):存放到那里

        Returns:
            bool: True/False
        """
        if self.proxy_host:
            status = os.system("cd " + file_path + " && git config --global http.proxy " + \
                               self.proxy_host + " && git config --global https.proxy " + \
                               self.proxy_host + " && git clone https://github.com/" + github_author + "/" + github_project + ".git")
        else:
            status = os.system("cd " + file_path + " && git config --global --unset http.proxy " + \
                               " && git config --global --unset https.proxy " + \
                               " && git clone https://github.com/" + github_author + "/" + github_project + ".git")
        if status == 0:
            return True
        return False

    def file_download(self, url="", file_path="", file_name="", is_zip_extract=False, retry=3, is_wget=False,
                      github_author="", github_project=""):
        """下载文件主方法(推荐调用)

        Args:
            url(str): url
            file_path(str): 文件存放在哪里
            file_name(str): 文件名称
            is_zip_extract(bool): 是否解压
            retry(int): 重试次数
            is_wget(bool): 是否用wget
            github_author(str): 项目作者
            github_project(str): 项目名称

        Returns:
            bool: True/False
        """
        file_name = os.path.basename(urlparse(url).path) if file_name == "" else file_name
        file_path = os.getcwd() if file_path == "" else file_path

        try:
            if is_wget:
                while retry > 0:
                    try:
                        print("DOWNLOAD %s from %s %s" % (file_name, url, retry))
                        if os.path.exists(os.path.join(file_path, file_name)):
                            os.remove(os.path.join(file_path, file_name))
                        if self.file_download_once(url=url, file=os.path.join(file_path, file_name)):
                            # 解压文件
                            if is_zip_extract == True:
                                uncompress(src_file=os.path.join(file_path, file_name), dest_dir_path=file_path)
                            return True
                    except Exception as e:
                        print("[DOWNLOAD ERROR] %s error:%s" % (url, repr(e)))
                    retry = retry - 1

            elif github_author:
                while retry > 0:
                    try:
                        src = str(github_author + github_project)
                        print("DOWNLOAD github from %s %s" % (src, retry))
                        if os.path.exists(os.path.join(file_path, github_project)):
                            shutil.rmtree(os.path.join(file_path, github_project))
                        if self.file_download_github(github_author=github_author, github_project=github_project, file_path=file_path):
                            return True
                    except Exception as e:
                        print("[DOWNLOAD ERROR] %s error:%s" % (url, repr(e)))
                    retry = retry - 1

            else:
                while retry > 0:
                    try:
                        print("DOWNLOAD %s from %s %s" % (file_name, url, retry))

                        r = self.file_download_once(url=url)
                        if r.status_code == 200:
                            with open(os.path.join(file_path, file_name), 'wb') as f:
                                shutil.copyfileobj(r.raw, f) if r.headers[
                                                                    "content-type"] == "application/x-zip-compressed" else f.write(
                                    r.content)
                            if is_zip_extract == True:
                                uncompress(src_file=os.path.join(file_path, file_name), des_dir_path=file_path)
                            return True
                        else:
                            print(r.status_code)
                    except Exception as e:
                        print("[DOWNLOAD ERROR] %s error:%s" % (url, repr(e)))
                    retry = retry - 1

        except Exception as e:
            print(repr(e))
        return False



# https://selenium-python.readthedocs.io/page-objects.html
# https://www.selenium.dev/zh-cn/documentation/
# 封装 selenium
class ChromeUtils:
    """
    ChromeUtils 基于 selenium 库进行的封装
    """
    def __init__(self, timeout: int, is_ssl_verify: bool=False, is_chrome_headless:bool = False, is_undetected_chromedriver:bool = False, proxy=None):
        self.timeout = timeout  # 请求超时时间
        self.is_ssl_verify = is_ssl_verify  # 是否验证SSL证书
        self.is_chrome_headless = is_chrome_headless # Linux下 is_chrome_headless为True
        self.is_undetected_chromedriver = is_undetected_chromedriver

        # 该参数代理是为了需要用固定ip的爬虫
        self.proxy = proxy # http://xxxxxx
        self.driver = self.get_chrome_driver(proxy)



    def get_chrome_driver(self, proxy=None):
        """获得一个chrome驱动

        Args:
            proxy(str): 代理

        Returns:
            chrome驱动

        """
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

        # 隐藏浏览器特征
        with open('./stealth.min.js') as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

        # 反屏蔽
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })

        return driver




    def refresh_chrome(self):
        """重启浏览器

        Returns:
            bool: 重启成功返回True，否则返回False

        """
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
                retry_time -= 1
                error = str(e)
                time.sleep(time_sleep)
        print("ERROR", str(error))
        return False



    def get_page_source(self, url, time_sleep=0, retry_count=3, proxy=""):
        """获得网页源码

        Args:
            url(str): 请求的url
            time_sleep(int): 页面会在time_sleep时间后获得源码
            retry_count(int): 重试次数，针对<html><head></head><body></body></html>情况
            proxy(str): 代理

        Returns:
            dict: {"error":"异常","content":"网页源码","url":"请求的url"}

        """

        # proxy = http://xxxx
        if proxy != "":
            if not self.driver is None:
                self.driver.quit()
            self.driver = self.get_chrome_driver(proxy)

        print(f"{get_nowdatetime()} Get {url}")


        while retry_count:
            retry_count -= 1
            if self.driver is None:
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

                if not self.refresh_chrome():
                    return {"error": "重启chrome失败","content": "","url": url}

                try:
                    self.driver.get(url)
                except Exception as e:
                    self.driver.execute_script("window.stop()")
                    return {"error":e,
                            "content":"",
                            "url":url}
            time.sleep(time_sleep)
            text = self.driver.page_source
            if text == "<html><head></head><body></body></html>":
                continue
            if text:
                return {"error": "",
                        "content": text,
                        "url": self.driver.current_url}
            else:
                return {"error": "没有获得 page_source",
                        "content": "",
                        "url": self.driver.current_url}

        return {"error": "",
         "content": "",
         "url": self.driver.current_url}


    def close(self):
        """关闭Chrome驱动

        """
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
