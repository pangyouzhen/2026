#! /home/pang/project/2025/venv310/bin/python3
import argparse
import re
from datetime import datetime
from pprint import pprint
from typing import Optional

import requests
from bs4 import BeautifulSoup
from loguru import logger
from playwright.sync_api import Playwright, expect, sync_playwright
from retry import retry

parser = argparse.ArgumentParser(description="获取市场情绪")
parser.add_argument("--path",default="./data/cls_zt", help="获取涨停数据")
# 输入日期格式 2023-08-04
parser.add_argument("--date", default=str(datetime.today().date()))
args = parser.parse_args()
print(args)
# @retry(Exception, tries=3, delay=2)
def run(playwright: Playwright,date,img_path) -> None:
    # date: 2026-01-24
    dt = datetime.strptime(date, "%Y-%m-%d")

    # 手动去掉前导零
    month = str(int(dt.strftime("%m")))  # 或直接 dt.month
    day = str(int(dt.strftime("%d")))    # 或直接 dt.day

    date_result = f"{month}月{day}日"
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.cls.cn/telegraph")
    page.get_by_text("加红").click()
    page.get_by_role("textbox", name="请输入要搜索的信息").click()
    page.get_by_role("textbox", name="请输入要搜索的信息").fill("%s涨停分析"%date_result)
    page.get_by_role("textbox", name="请输入要搜索的信息").press("Enter")

        # 获取所有 src
    with page.expect_popup() as page2_info:
        page.get_by_role("link", name="【%s涨停分析】财联社%s电，今日全市场共"%(date_result,date_result)).click()
    page2 = page2_info.value
    page2.wait_for_timeout(10000)  # 强制等待 3 秒
    src_list = [img.get_attribute("src") for img in page2.locator("img").all()]

    # 打印整个列表
    print(src_list)

    # 或者检查是否为空后再打印第一个
    if src_list:
        print(f"第一张图是: {src_list[0]}")
    page.wait_for_timeout(10000)
    ind_ = {2:1,1:0}
    for ind,v in ind_.items():
        url = src_list[ind]
        html = requests.get(url)
        img_name = str(date)
        print(img_name)
        with open("%s/%s_zt_analyse_%s.png" % (img_path, img_name,v), "wb") as file:
                file.write(html.content)
        print("获取今日涨停分析成功")
    # imgs = page.locator("img").all()
    # # .nth(2).get_attribute("src")
    # for i in imgs:
    #     print(i.get_attribute("src"))
    # print(src)
    # with page.expect_popup() as page1_info:
    #     page.get_by_role("link", name="【1月23日涨停分析】财联社1月23日电，今日全市场共").click()
    # page1 = page1_info.value
    # page1.locator("div:nth-child(2) > .telegraph-image-thumbnail").click()
    # page1.locator(".telegraph-image-box-mask").click()
    # page1.locator(".telegraph-image-box-mask").click()
    # page1.locator(".telegraph-image-box-mask").click()
    # page1.get_by_role("img").nth(3).click()
    # page1.locator("div:nth-child(2) > .telegraph-image-thumbnail").click()
    # page1.locator(".telegraph-image-box-mask").click()
    # page1.get_by_role("img").nth(3).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright,args.date,args.path)
