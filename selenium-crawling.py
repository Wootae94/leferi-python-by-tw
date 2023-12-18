import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import quote
import chromedriver_autoinstaller as AutoChrome
import shutil
from webdriver_manager.chrome import ChromeDriverManager


def chromedriver_update():
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
    print(f'현재 버전은 {chrome_ver}입니다.')
    current_list = os.listdir(os.getcwd())
    print(f'전체 객체 확인 : {current_list}')
    chrome_list = []
    for i in current_list:
        path = os.path.join(os.getcwd(), i)
        print(f'객체 경로 설정 : {path}')
        if os.path.isdir(path):
            print(f'[폴더확인]')
            if 'chromedriver.exe' in os.listdir(path):
                print(f'[크롬드라이버확인]')
                chrome_list.append(i)
    print(f'크롬드라이버가 들어있는 폴더명 : {chrome_list} / 최신버전인 {chrome_ver} 제외')
    old_version = list(set(chrome_list) - set([chrome_ver]))
    print(f'구버전이 포함된 폴더명 : {old_version}')

    for i in old_version:
        path = os.path.join(os.getcwd(), i)
        print(f'구버전이 포함된 폴더의 전체 경로: {path} 삭제 진행')
        shutil.rmtree(path)

    if not chrome_ver in current_list:
        print("최신 버전 크롬드라이버가 없습니다.")
        print("크롬드라이버 다운로드 실행")
        AutoChrome.install(True)
        print("크롬드라이버 다운로드 완료")
    else:
        print("크롬드라이버 버전이 최신입니다.")


def get_video_url_list_from_youtube(search_word_list):
    # 현재 크롬 버전에 맞는 크롬드라이버 버전 다운로드
    chromedriver_update()
    # 설치된 드라이버 설정
    driver = webdriver.Chrome(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
    options.add_argument('headless')  # headless 모드 설정
    options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    options.add_argument("disable-gpu")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # 속도 향상을 위한 옵션 해제
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
                                                        'geolocation': 2, 'notifications': 2,
                                                        'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                                                        'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                                                        'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                        'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
    options.add_experimental_option('prefs', prefs)
    driver.maximize_window()
    video_list = []
    search_word_list = search_word_list
    for search_word in search_word_list:
        # 유튜브 검색 URL
        searchUrl = f"https://www.youtube.com/results?search_query={search_word}"
        driver.get(searchUrl)
        time.sleep(0.5)
        # 스크롤 25번 내리기
        pageDownNum = 25
        while pageDownNum > 0:
            body = driver.find_element_by_tag_name('body')
            time.sleep(0.5)
            body.send_keys(Keys.PAGE_DOWN)
            pageDownNum -= 1

        # 비디오 섹션에서 비디오 목록 찾기
        print("스크롤 끝")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        videos_sections = soup.find_all("ytd-item-section-renderer")
        time.sleep(0.5)

        for section in videos_sections:
            tmp = section.find_all("ytd-video-renderer")
            for i in tmp:
                video_list.append(i)

            time.sleep(0.5)
    print(len(video_list))


if __name__ == '__main__':
    get_video_url_list_from_youtube(["백엔드", "개발"])
