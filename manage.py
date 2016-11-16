# coding=utf-8

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
    print "test."


@manager.command
def get_main_page_data(debug=False):
    """#get main page data, and save the result to file ./api-data/main_page_data.json"""

    helper.remove_file(config.FILENAME_MAIN_PAGE_DATA)  # 先删除可能已存在的文件后, 再重新保存
    helper.create_dir(config.SAVE_FILE_DIR)

    t0 = time.time()
    url = helper.get_main_page_url()
    content = helper.get_url_content(url, debug)  # 获取首页的一级页面列表(包含年级列表,滚动图列表,学习计划列表等)
    if content is not None:
        helper.save_content_to_file(config.FILENAME_MAIN_PAGE_DATA, content)
        helper.my_print(content, debug)

    print 'Done. %f seconds cost.' % (time.time() - t0)


@manager.command
def get_second_page_data(debug=False):
    """#get second page data, and save result to file ./api-data/second_page_data.json"""

    helper.remove_file(config.FILENAME_SECOND_PAGE_DATA)
    helper.remove_file(config.FILENAME_SECOND_PAGE_SECTIONIDS_DATA)
    helper.create_dir(config.SAVE_FILE_DIR)

    t0 = time.time()
    helper.my_print("total has %d grades...\n", len(config.GRADES))

    for grade in config.GRADES:
        time.sleep(config.SLEEP_TIME)

        url = helper.get_second_page_url(grade=grade)
        content = helper.get_url_content(url, debug)  # 获取知识章节列表
        if content is not None:
            helper.save_content_to_file(config.FILENAME_SECOND_PAGE_DATA, content)
            helper.my_print("%s:\n%s" % (grade, content), debug)

            # 获取知识章节对应的ID列表
            json_data = json.loads(content, encoding='utf-8')
            for course_list in json_data['list']:
                for course in course_list['list']:
                    section_id = course['courseSectionID']
                    helper.save_content_to_file(config.FILENAME_SECOND_PAGE_SECTIONIDS_DATA, section_id)
                    helper.my_print(section_id, debug)

            helper.my_print("", debug)

    print 'Done. %f seconds cost.' % (time.time() - t0)


@manager.command
def get_third_page_data(debug=False):
    """#get third page data, and save result to file ./api-data/third_page_data.json"""

    helper.remove_file(config.FILENAME_THIRD_PAGE_DATA)
    helper.remove_file(config.FILENAME_THIRD_SECTIONIDS_DATA)
    helper.create_dir(config.SAVE_FILE_DIR)

    t0 = time.time()
    with open(config.FILENAME_SECOND_PAGE_SECTIONIDS_DATA) as f:
        i = 0
        lines = f.readlines()
        helper.my_print("total has %d chapters...\n", len(lines))

        for line in lines:
            i += 1
            section_id = str(int(line))
            time.sleep(config.SLEEP_TIME)

            url = helper.get_third_page_url(section_id)
            content = helper.get_url_content(url, debug)  # 根据某个章节的 sectionID, 获取其知识点列表
            if content is not None:
                helper.save_content_to_file(config.FILENAME_THIRD_PAGE_DATA, content)
                helper.my_print("%d:\n%s" % (i, content), debug)

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

    print 'Done. %f seconds cost.' % (time.time() - t0)


@manager.command
def get_question_data(debug=False):
    """#get question data, and ave result to file ./api-data/question_data.json"""

    helper.remove_file(config.FILENAME_QUESTION_DATA)
    helper.create_dir(config.SAVE_FILE_DIR)

    t0 = time.time()
    with open(config.FILENAME_THIRD_SECTIONIDS_DATA) as f:
        i = 0
        lines = f.readlines()
        helper.my_print("total has %d sections...\n", len(lines))

        for line in lines:
            i += 1
            json_data = json.loads(line)
            section_id = json_data['courseSectionID']
            time.sleep(config.SLEEP_TIME)

            url = helper.get_question_url(section_id)
            content = helper.get_url_content(url, debug)  # 根据知识点的 sectionID, 获取题目对表
            if content is not None:
                helper.save_content_to_file(config.FILENAME_QUESTION_DATA, content)
                helper.my_print("%d:\n%s" % (i, content), debug)

            helper.my_print("", debug)

    print 'Done. %f seconds cost.' % (time.time() - t0)


if __name__ == '__main__':
    manager.run()
