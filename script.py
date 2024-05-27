from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# قائمة البروكسيات
proxies = [
    "20.219.177.85:3129",
    "35.185.196.38:3128",
    "45.61.163.2:80",
    "49.12.150.91:8080",
    "20.170.91.53:443",
    "72.10.160.170:33147",
    "185.217.136.67:1337",
    "67.43.236.19:2167",
    "69.197.135.242:61886",
    "13.56.81.94:3128",
    "71.86.129.131:8080",
    "71.86.129.168:8080",
    "71.86.129.130:8080",
    "71.86.129.137:8080",
    "43.134.33.254:3128",
    "71.86.129.160:8080",
    "72.10.160.174:21013",
    "20.37.207.8:8080",
    "71.86.129.152:8080",
    "71.86.129.167:8080",
    "43.134.229.98:3128",
    "77.238.235.219:8080",
    "71.86.129.153:8080",
    "71.86.129.162:8080",
    "184.104.213.156:8888",
    "67.43.228.250:32897",
    "144.76.225.182:3128",
    "144.76.64.184:3128",
    "200.174.198.86:8888",
    "72.10.160.173:3985",
    "223.135.156.183:8080",
    "203.189.88.156:80",
    "148.135.6.246:2233",
    "71.86.129.180:8080",
    "148.72.165.7:10529",
    "20.235.159.154:80",
    "72.10.164.178:1075",
    "67.43.236.21:8873",
    "144.217.119.85:3207",
    "67.43.236.22:33169",
    "13.212.145.2:48540",
    "160.72.98.165:3128",
    "222.243.174.132:81",
    "124.167.20.48:7777",
    "67.43.228.252:3187",
    "80.66.81.39:4000",
    "154.127.240.126:64001",
    "154.127.240.125:64002",
    "154.127.240.117:64003",
    "154.127.240.114:64002",
    "109.123.230.171:3128",
    "195.24.157.66:4018",
    "195.68.158.11:3129",
    "158.69.185.37:3129",
    "192.99.182.243:3128",
    "154.127.240.118:64001",
    "154.127.240.123:64001",
    "43.134.32.184:3128",
    "154.127.240.120:64002",
    "4.155.2.13:9480",
    "20.33.5.27:8888",
    "205.196.184.69:50704",
    "117.177.63.75:8118",
    "135.181.102.118:7117",
    "20.44.190.150:3129",
    "209.121.164.50:31147",
    "154.127.240.121:64003",
    "154.127.240.113:64002",
    "154.127.240.124:64003",
    "154.127.240.122:64002",
    "157.159.10.86:80",
    "154.236.179.229:1981",
    "144.217.131.61:3148",
    "20.204.214.23:3129",
    "126.74.234.11:80",
    "20.219.177.38:3129",
    "20.219.180.105:3129",
    "20.204.212.76:3129",
    "20.204.212.45:3129",
    "20.44.188.17:3129",
    "20.219.180.149:3129",
    "20.219.183.188:3129",
    "20.44.189.184:3129",
    "157.245.1.60:3128",
    "188.121.128.246:10186",
    "139.180.182.111:80",
    "210.87.125.146:8080",
    "179.50.90.166:8513",
    "152.67.0.109:80",
    "88.200.195.120:80",
    "20.219.178.121:3129",
    "20.204.214.79:3129",
    "91.229.67.77:8083",
    "146.190.57.198:8081",
    "23.122.184.9:8888",
    "113.179.83.118:3128",
    "20.219.235.172:3129",
    "20.204.190.254:3129",
    "14.194.136.125:80",
    "203.190.44.201:8080"
]

def get_video_duration(driver):
    try:
        # جلب مدة الفيديو من الصفحة
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

    proxy_options = {
        'proxy': {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options, seleniumwire_options=proxy_options)
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

tiktok_video_url = "https://www.tiktok.com/@abdellaherguig0/video/7373608769353239814?is_from_webapp=1&sender_device=pc&web_id=7373345132706039328"

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(tiktok_video_url)
watch_time = get_video_duration(driver)
driver.quit()

total_duration_hours = 6
manage_viewers(tiktok_video_url, proxies, total_duration_hours)
