# coding=utf-8

from __future__ import print_function
import json
import time

from flask_script import Manager

import config
import helper
from app import app


manager = Manager(app)


@manager.command
def test():
    """do a test"""
    print("test.")


@manager.command
def get_main_page_data(debug=False):
    """#get main page data, and save the result to file ./api-data/main_page_data.json"""

    helper.remove_file(config.FILENAME_MAIN_PAGE_DATA)  # 先删除可能已存在的文件后, 再重新保存
    helper.create_dir(config.SAVE_FILE_DIR)

    t0 = time.time()
    url = helper.get_main_page_url()
    content = helper.get_url_content(url)  # 获取首页的一级页面列表(包含年级列表,滚动图列表,学习计划列表等)
    if content is None:
        helper.my_print_error("main_page_data is None.")
    else:
        helper.save_content_to_file(config.FILENAME_MAIN_PAGE_DATA, content)
        helper.my_print(content, debug)

    print('Done. %f seconds cost.' % (time.time() - t0))


@manager.command
def get_second_page_data(debug=False):
    """#get second page data, and save result to file ./api-data/second_page_data.json"""

    t0 = time.time()
    helper.remove_file(config.FILENAME_SECOND_PAGE_DATA)
    helper.remove_file(config.FILENAME_SECOND_PAGE_SECTIONIDS_DATA)
    helper.create_dir(config.SAVE_FILE_DIR)
    helper.my_print("total has %d grades...\n" % len(config.GRADES), debug)

    for grade in config.GRADES:
        time.sleep(config.SLEEP_TIME)
        helper.my_print("%s:" % grade, debug)

        url = helper.get_second_page_url(grade=grade)
        content = helper.get_url_content(url)  # 获取知识章节列表
        if content is None:
            helper.my_print_error("the content is None.")
        else:
            helper.save_content_to_file(config.FILENAME_SECOND_PAGE_DATA, content)
            helper.my_print(content, debug)

            # 获取知识章节对应的ID列表
            json_data = json.loads(content, encoding='utf-8')
            for course_list in json_data['list']:
                for course in course_list['list']:
                    section_id = course['courseSectionID']
                    helper.save_content_to_file(config.FILENAME_SECOND_PAGE_SECTIONIDS_DATA, section_id)
                    helper.my_print(section_id, debug)

        helper.my_print("", debug)

    print('Done. %f seconds cost.' % (time.time() - t0))


@manager.command
def get_third_page_data(debug=False):
    """#get third page data, and save result to file ./api-data/third_page_data.json"""

    t0 = time.time()
    helper.remove_file(config.FILENAME_THIRD_PAGE_DATA)
    helper.remove_file(config.FILENAME_THIRD_SECTIONIDS_DATA)
    helper.create_dir(config.SAVE_FILE_DIR)

    with open(config.FILENAME_SECOND_PAGE_SECTIONIDS_DATA) as f:
        i = 0
        lines = f.readlines()
        helper.my_print("total has %d chapters...\n" % len(lines), debug)

        for line in lines:
            i += 1
            section_id = str(int(line))
            helper.my_print("line:%d sectionID:%s" % (i, section_id), debug)

            time.sleep(config.SLEEP_TIME)
            url = helper.get_third_page_url(section_id)
            content = helper.get_url_content(url)  # 根据某个章节的 sectionID, 获取其知识点列表
            if content is None:
                helper.my_print_error("the content is None.")
            else:
                helper.save_content_to_file(config.FILENAME_THIRD_PAGE_DATA, content)
                helper.my_print(content, debug)

                # 获取知识点对应的课程ID列表(用于根据课程ID, 获取题目列表)
                json_data = json.loads(content)
                for course in json_data['list']:
                    course_dic = {
                        'courseSectionID': course['courseSectionID'],
                        'sectionName': course['sectionName'],
                        'parentID': course['parentID']
                    }

                    data = json.dumps(course_dic, ensure_ascii=False)
                    helper.save_content_to_file(config.FILENAME_THIRD_SECTIONIDS_DATA, data)
                    helper.my_print(data, debug)

            helper.my_print("", debug)

    print('Done. %f seconds cost.' % (time.time() - t0))


@manager.command
def get_question_data(debug=False, start=1, count=0):
    """#get question data, and save result to file ./api-data/question_data.json"""

    t0 = time.time()
    with open(config.FILENAME_THIRD_SECTIONIDS_DATA) as f:
        i = 0
        lines = f.readlines()
        line_count = len(lines)

        # 检查开始索引参数 start
        try:
            start_index = int(start)
        except ValueError as e:
            helper.my_print_error('Error: %s\n the "start" param must be a Integer number!' % e)
            return
        else:
            if start_index < 1 or start_index > line_count:
                helper.my_print_error('Error:  the "start" param must in range(1, len(lines)+1)')
                return

        # 检查获取条目参数 count
        try:
            limit_count = int(count)
        except ValueError as e:
            helper.my_print_error('Error: %s\n the "count" param must be a Integer number!' % e)
            return
        else:
            if limit_count <= 0 or (start_index - 1 + limit_count) > line_count:
                limit_count = line_count - start_index + 1

        if start_index == 1:  # 当 start_index 值为1时, 表示重新开始获取, 此时应先清除之间存在的数据文件
            helper.remove_file(config.FILENAME_QUESTION_DATA)

        helper.create_dir(config.SAVE_FILE_DIR)
        helper.my_print("total has %d sections...\n" % line_count, debug)

        for line in lines:
            i += 1
            if i < start_index:
                continue
            elif i >= (start_index + limit_count):
                break

            json_data = json.loads(line)
            section_id = json_data['courseSectionID']
            helper.my_print("line:%d sectionID:%s" % (i, section_id), debug)

            time.sleep(config.SLEEP_TIME)
            url = helper.get_question_url(section_id)
            content = helper.get_url_content(url)  # 根据知识点的 sectionID, 获取题目对表
            if content is None:  # 若发生了异常时, 直接退出
                helper.my_print_error("the content is None.")
                helper.my_print_error("An Exception has happen. get_question_data will be exit. "
                                      "the next start_index should be %d" % i)
                break
            else:
                result_data = json.loads(content)
                if result_data['code'] != '99999':  # 若返回码不是表示"成功"时, 直接退出
                    helper.my_print_error("result code is not 99999. get_question_data will be exit. "
                                          "the next start_index should be %d" % i)
                    break

                helper.save_content_to_file(config.FILENAME_QUESTION_DATA, content)
                helper.my_print(content, debug)
                helper.my_print("", debug)

    print('Done. %f seconds cost.' % (time.time() - t0))


if __name__ == '__main__':
    manager.run()
