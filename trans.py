# -*- coding: utf-8 -*-


import argparse
import re
import openai
from tqdm import tqdm

import os
import tempfile
import shutil

import configparser

from io import StringIO
import random
import json
import chat
import pyvtt 

import chardet

jsonfile = "2-develop-your-pieces.en_US_process.json"
# 从文件中加载已经翻译的文本
translated_dict = {}
try:
    with open(jsonfile, "r", encoding="utf-8") as f:
        translated_dict = json.load(f)
except FileNotFoundError:
    pass

def split_text(text):
    # 使用正则表达式匹配输入文本的每个字幕块（包括空格行）
    blocks = re.split(r'(\n\s*\n)', text)

    # 初始化短文本列表
    short_text_list = []
    # 初始化当前短文本
    short_text = ""
    # 遍历字幕块列表
    for block in blocks:
        # 如果当前短文本加上新的字幕块长度不大于1024，则将新的字幕块加入当前短文本
        if len(short_text + block) <= 600:
            short_text += block
        # 如果当前短文本加上新的字幕块长度大于1024，则将当前短文本加入短文本列表，并重置当前短文本为新的字幕块
        else:
            short_text_list.append(short_text)
            short_text = block
    # 将最后的短文本加入短文本列表
    short_text_list.append(short_text)
    return short_text_list


def is_translation_valid(original_text, translated_text):
    def get_index_lines(text):
        lines = text.split('\n')
        index_lines = [line for line in lines if re.match(
            r'^\d+$', line.strip())]
        return index_lines

    original_index_lines = get_index_lines(original_text)
    translated_index_lines = get_index_lines(translated_text)

    print(original_text, original_index_lines)
    print(translated_text, translated_index_lines)

    return original_index_lines == translated_index_lines


def translate_text(text):
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            prompt = f"Translate the following subtitle text into {language_name}, but keep the subtitle number and timeline unchanged. IMPORTANT: Do not merge subtitle text in different subtitle numbers: \n{text}"
            print(prompt)
            response = chat.create(prompt)

            print("=======")

            t_text = (
                response
                .get("content")
                # .encode("utf8")
                # .decode()
            )
            print(t_text)

            return t_text

            # if is_translation_valid(text, t_text):
            #     return t_text
            # else:
            #     retries += 1
            #     print(f"Invalid translation format. Retrying ({retries}/{max_retries})")

        except Exception as e:
            import time
            sleep_time = 60
            time.sleep(sleep_time)
            retries += 1
            print(
                e, f"will sleep {sleep_time} seconds, Retrying ({retries}/{max_retries})")

    print(
        f"Unable to get a valid translation after {max_retries} retries. Returning the original text.")
    return text


def translate_and_store(text):
    # 如果文本已经翻译过，直接返回翻译结果
    if text in translated_dict:
        return translated_dict[text]


def split_blocks(text):
    blocks = re.split(r'(\n\s*\n)', text.strip())
    return [block.split('\n') for block in blocks if block.strip()]

def replace_text(text1, text2):
    blocks1 = split_blocks(text1)
    blocks2 = split_blocks(text2)

    if len(blocks1) != len(blocks2):
        print("警告！！！长度不一致")
        blocks1.pop(0)

    replaced_lines = []

    for block1, block2 in zip(blocks1, blocks2):
        replaced_lines.extend(block1[:2])  # Index and timestamp
        replaced_lines.extend(block2[2:])  # Chinese content
        replaced_lines.append('')  # Add an empty line

    return '\n'.join(replaced_lines).strip()

def merge_text(text1, text2):
    blocks1 = split_blocks(text1)
    blocks2 = split_blocks(text2)

    if len(blocks1) != len(blocks2):
        print("警告！！！长度不一致")
        blocks1.pop(0)

    merged_lines = []

    for block1, block2 in zip(blocks1, blocks2):
        merged_lines.extend(block1[:2])  # Index and timestamp
        merged_lines.extend(block1[2:])  # English content
        merged_lines.extend(block2[2:])  # Chinese content
        merged_lines.append('')  # Add an empty line

    return '\n'.join(merged_lines).strip()

def trans():
    # 初始化翻译后的文本
    text = ""
    translated_text = ""

    filename = "2-develop-your-pieces.en_US.vtt"
    filename_zh = "test.zh_CN.vtt"
    filename_bi = "test.bilingual.vtt"
    

    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    # 将文本分成不大于1024字符的短文本list
    short_text_list = split_text(text)
    # 遍历短文本列表，依次翻译每个短文本
    for short_text in tqdm(short_text_list):
        print((short_text))
        # 翻译当前短文本
        translated_short_text = translate_and_store(short_text)

        # 将当前短文本和翻译后的文本加入总文本中
        translated_text += f"{translated_short_text}\n\n"
        # print(short_text)
        print(translated_short_text)

    # 读取英文字幕文件
    subs = pyvtt.open(filename)
    subs_translated = pyvtt.from_string(translated_text)

    subs_translated.save(filename_zh, include_indexes=True)
    
    # blocks1 = split_blocks(text)
    # blocks2 = split_blocks(translated_text)

    # result = replace_text(text, translated_text)
    # # 将翻译后的文本写入srt文件
    # with open(filename_zh, "w", encoding="utf-8") as f:
    #     f.write(result)
    
    # result2 = merge_text(text, translated_text)
    # # 将翻译后的文本写入srt文件
    # with open(filename_bi, "w", encoding="utf-8") as f:
    #     f.write(result2)

    return


if __name__ == "__main__":
    trans()