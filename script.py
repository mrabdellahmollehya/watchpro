from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# قراءة البروكسيات من ملف
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def get_video_duration(driver):
    try:
        # حاول الحصول على مدة الفيديو (قد تختلف الطريقة حسب الموقع)
        duration_element = driver.find_element_by_xpath('//*[contains(@class, "video-duration")]')
        duration_text = duration_element.text
        minutes, seconds = map(int, duration_text.split(':'))
        duration_seconds = minutes * 60 + seconds
        return duration_seconds
    except Exception as e:
        print("Error getting video duration:", e)
        return 0

def create_virtual_viewer(url, proxy, watch_time):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--mute-audio")

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    print(f"Virtual viewer started watching {url} with proxy {proxy}")
    time.sleep(watch_time)
    driver.quit()
    print("Virtual viewer stopped watching")

def manage_viewers(url, proxies, total_duration_hours=6):
    start_time = time.time()
    end_time = start_time + total_duration_hours * 3600

    while time.time() < end_time:
        for proxy in proxies:
            create_virtual_viewer(url, proxy, watch_time)
        time.sleep(watch_time)

if __name__ == "__main__":
    tiktok_video_url = "https://www.tiktok.com/@abdellaherguig0/video/7373608769353239814?is_from_webapp=1&sender_device=pc&web_id=7373345132706039328"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(tiktok_video_url)
    watch_time = get_video_duration(driver)
    driver.quit()

    proxies = load_proxies('proxies.txt')
    total_duration_hours = 6
    manage_viewers(tiktok_video_url, proxies, total_duration_hours)
