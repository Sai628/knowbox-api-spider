# coding=utf-8

from __future__ import print_function
import os

import requests

import config


# 获取"速算闯关-年级列表(一级页面)"的 URL
def get_main_page_url():
    url = config.API_GET_MAIN_PAGE + "?"
    for k in config.BASE_PARAMS.keys():
        url += '%s=%s&' % (k, config.BASE_PARAMS[k])
    return url[0:-2]


# 获取"闯关-获取知识章节列表(二级页面)"的 URL
def get_second_page_url(grade, type_='Stone'):
    url = config.API_GET_SECOND_PAGE + '?'
    for k in config.BASE_PARAMS.keys():
        url += '%s=%s&' % (k, config.BASE_PARAMS[k])
    url += 'grade=%s&type=%s' % (grade, type_)
    return url


# 获取"闯关-获取关卡列表(三级页面)"的 URL
def get_third_page_url(section_id, game_era='Stone'):
    url = config.API_GET_THIRD_PAGE + '?'
    for k in config.BASE_PARAMS.keys():
        url += '%s=%s&' % (k, config.BASE_PARAMS[k])
    url += 'sectionID=%s&gameEra=%s' % (section_id, game_era)
    return url


# 获取"闯关-获取某关卡的题目列表"的 URL
def get_question_url(section_id):
    url = config.API_GET_QUESTION + '?'
    for k in config.BASE_PARAMS.keys():
        url += '%s=%s&' % (k, config.BASE_PARAMS[k])
    url += 'sectionID=%s' % section_id
    return url


def get_url_content(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        my_print_error("Error: %s\nget_url_content -- %s" % (e, url))
        return None


def save_content_to_file(file_path, content):
    f = open(file_path, 'a')
    f.write(content + '\n')
    f.close()


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def my_print(text, debug=False):
    if debug:
        print(text)


def my_print_error(text):
    print('\033[0;31;40m%s' % text)
