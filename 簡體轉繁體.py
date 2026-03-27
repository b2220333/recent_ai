#!/usr/bin/env python3
# encoding: utf-8

from opencc import OpenCC

# 1. 初始化轉換器 ('s2t' 代表 Simplified to Traditional)
cc = OpenCC('s2t')

# 2. 讀取並轉換
try:
    with open('words.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open('words.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            # 執行轉換並寫入
            traditional_line = cc.convert(line)
            f.write(traditional_line)
            
    print("轉換成功！現在 words.txt 全都是繁體字了。")

except FileNotFoundError:
    print("錯誤：找不到 words.txt")