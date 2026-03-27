#!/usr/bin/env python3
# encoding: utf-8

import random
import os

# 設定檔案路徑
SOURCE_FILE = "words.txt"

def load_words(file_path):
    word_list = []
    if not os.path.exists(file_path):
        print(f"錯誤：找不到 {file_path}")
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ',' not in line:
                continue
            
            # 使用 rsplit(',', 1) 確保只切出最後一個英文單字，解決多個逗號問題
            parts = line.rsplit(',', 1)
            ch = parts[0].strip()
            en = parts[1].strip().lower()
            
            # 初始權重設為 1
            word_list.append({"ch": ch, "en": en, "weight": 1})
    return word_list

def main():
    word_list = load_words(SOURCE_FILE)
    if not word_list:
        return

    print("==============================")
    print("   黑客單字挑戰 (輸入 q 離開)   ")
    print("==============================")

    while True:
        # 根據權重計算機率
        weights = [w["weight"] for w in word_list]
        target = random.choices(word_list, weights=weights, k=1)[0]
        
        # 提問
        user_input = input(f"\n題目：【{target['ch']}】\n請輸入英文: ").strip().lower()

        if user_input == 'q':
            print("\n練習結束，繼續加油！")
            break

        # 判斷對錯
        if user_input == target['en']:
            print("✅ 正確！")
            # 答對了，降低權重（最低為 1）
            if target['weight'] > 1:
                target['weight'] -= 1
        else:
            print(f"❌ 錯誤！正確答案是: {target['en']}")
            # 答錯了，大幅增加權重（下次出現機率變高）
            target['weight'] += 5

if __name__ == "__main__":
    main()