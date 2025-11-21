from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date, timedelta
from mail import get_code
import pandas as pd
import time
import glob
import os


creds = os.getenv("NEXTBIKE_CREDS")
NEXTBIKE_USER  = creds.split("\n")[0]
NEXTBIKE_PASS  = creds.split("\n")[1]

REQUEST_TIMEOUT = 400  # lo que necesitas que aguante

def set_driver():    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    download_dir = "/tmp/downloads"
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 👉 ESTE es el que realmente usa urllib3
    try:
        driver.command_executor._client_config.timeout = REQUEST_TIMEOUT
        print("HTTP timeout de Selenium:", driver.command_executor._client_config.timeout)
    except Exception as e:
        print("No se pudo cambiar _client_config.timeout:", e)

    # (opcional) permitir descargas en headless
    try:
        driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": download_dir},
        )
    except Exception as e:
        print("No se pudo configurar setDownloadBehavior:", e)

    return driver, download_dir





def log_in_nextbike(driver, url):
    driver.get(url)

    driver.find_element(By.ID, "parameters[username]").send_keys(NEXTBIKE_USER)
    driver.find_element(By.ID, "parameters[password]").send_keys(NEXTBIKE_PASS)
    driver.find_element(By.ID, "login_post").click()

    time.sleep(1.5)
    
    verification_code = get_code()
    
    driver.find_element(By.ID, "parameters[otp_code]").send_keys(verification_code)
    driver.find_element(By.ID, "login_post").click() 


def get_dates():
    today = date.today()
    last_day_prev_month = today.replace(day=1) - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)

    return (
        first_day_prev_month.strftime("%Y-%m-%d 00:00"),
        last_day_prev_month.strftime("%Y-%m-%d 23:59")
    )                              


REQUEST_TIMEOUT = 400  # lo que necesitas que aguante

REQUEST_TIMEOUT = 400

def safe_get(driver, url, timeout=REQUEST_TIMEOUT):
    driver.set_page_load_timeout(timeout)
    try:
        driver.get(url)
    except TimeoutException:
        if url.endswith("410"):
            return
        raise Exception(f"La página {url} tardó más de {timeout} segundos en cargar.")




def download_from_nextbike(driver, download_dir, url):

    if url.endswith("410"):
        timeout = 5
    else:
        timeout = REQUEST_TIMEOUT
        
    safe_get(driver, url, timeout)

    start_date, end_date = get_dates()
    start_time = time.time()

    if url.endswith(("639", "641", "640")):
        driver.find_element(By.ID, "parameters[start_time]").send_keys(start_date)
        driver.find_element(By.ID, "parameters[end_time]").send_keys(end_date)

    elif url.endswith(("730", "129")):
        driver.find_element(By.ID, "parameters[start_date]").send_keys(start_date)
        driver.find_element(By.ID, "parameters[end_date]").send_keys(end_date)

    if not url.endswith("424"):
        driver.find_element(By.ID, "parameters[export_csv]").click()    
        driver.find_element(By.ID, "queries_view_get").click()

    file_path = None
    for _ in range(60):
        files = glob.glob(os.path.join(download_dir, "*.csv"))
        new_files = [f for f in files if os.path.getmtime(f) > start_time]

        if new_files:
            file_path = max(new_files, key=os.path.getmtime)
            break

        time.sleep(1)

    if not file_path: raise RuntimeError("No se encontró ningún CSV generado por Nextbike")

    return pd.read_csv(file_path, sep='\t', encoding='utf-8')


def run_nextbike_etl(url):
    driver, download_dir = set_driver()
    try:
        log_in_nextbike(driver, url)
        df = download_from_nextbike(driver, download_dir, url)
        return df
    finally: driver.quit()
