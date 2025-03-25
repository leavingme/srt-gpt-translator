# -*- coding: utf-8 -*-
import sys
import pyvtt          # 用于读取 srt 格式的字幕文件
from googletrans import Translator    # 用于翻译英文成中文

def usage():
    print("Usage: ./srt_trans.py test.en_US.vtt test.zh_CN.vtt")

def main():
    print(sys.argv)

    file_src = sys.argv[1]
    file_dst = sys.argv[2]

    # 读取英文字幕文件
    subs = pyvtt.open(file_src)
    
    # 初始化翻译器
    translator = Translator()

    # 新建中文字幕文件
    out_subs = pyvtt.WebVTTFile()

    # 循环翻译每一个字幕并写入新的字幕文件
    for i in range(len(subs)):
        sub = subs[i]
        original_text = sub.text
        chinese_text = translator.translate(original_text, src='en', dest='zh-cn').text
        new_sub = pyvtt.WebVTTItem(sub.index, sub.start, sub.end, chinese_text)
        out_subs.append(new_sub)

    # 将翻译结果写入新的字幕文件
    out_subs.save(file_dst)

if __name__ == "__main__":
    main()