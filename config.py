# coding=utf-8


# 获取数据时, 调用API之间的间隔时间(防止过于频繁访问)
SLEEP_TIME = 0.5


# 获取数据后的文件保存路径
SAVE_FILE_DIR = './api-data'
FILENAME_MAIN_PAGE_DATA = SAVE_FILE_DIR + '/main_page_data.json'
FILENAME_SECOND_PAGE_DATA = SAVE_FILE_DIR + '/second_page_data.json'
FILENAME_SECOND_PAGE_SECTIONIDS_DATA = SAVE_FILE_DIR + '/second_page_section_ids.txt'
FILENAME_THIRD_PAGE_DATA = SAVE_FILE_DIR + '/third_page_data.json'
FILENAME_THIRD_SECTIONIDS_DATA = SAVE_FILE_DIR + '/third_page_section_ids.txt'
FILENAME_QUESTION_DATA = SAVE_FILE_DIR + '/question_data.json'


# API地址
API_DOMAIN = 'http://stuapi.knowbox.cn'
API_GET_MAIN_PAGE = API_DOMAIN + '/hurdle/section/get-main-page'
API_GET_SECOND_PAGE = API_DOMAIN + '/hurdle/section/get-second-page'
API_GET_THIRD_PAGE = API_DOMAIN + '/hurdle/section/get-third-page'
API_GET_QUESTION = API_DOMAIN + '/hurdle/section/get-questions'


# 请求基本请求参数
BASE_PARAMS = {
    'source': 'androidRCStudent',
    'version': '291',
    'channel': 'knowbox',
    'deviceId': '000000000000000',
    'deviceVersion': '4.4.4',
    'deviceType': 'Google%20Nexus%205%20-%204.4.4%20-%20API%2019%20-%201080x1920',
    'token': 'k2k4s6J577eYm4VCZFozQN6x3U5flA1Wnd6%2B0nH%2B%2Fwdf%2BgWH1erL9IypNye1q5oS',
    'kbparam': 'BB7E5D39627B961A7A3977CDEB544C56'
}


GRADES = ['FirstGrade', 'SecondGrade', 'ThirdGrade', 'FourthGrade', 'FifthGrade', 'SixthGrade']
