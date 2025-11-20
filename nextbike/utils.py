from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import glob
import os
from mail import get_code


# creds = os.getenv("NEXTBIKE_CREDS")
# NEXTBIKE_USER  = creds.split("\n")[0]
# NEXTBIKE_PASS  = creds.split("\n")[1]
NEXTBIKE_USER  = "pmedina"
NEXTBIKE_PASS  = "nPmse.52725"

def set_driver():

    # Crear carpeta temporal controlada por el script
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # ⬇⬇⬇ Aumentar timeouts ⬇⬇⬇
    # Timeout entre tu script y chromedriver (antes eran 120s)
    driver.command_executor.set_timeout(3000)   # por ejemplo 300 segundos

    # Timeout de carga de páginas
    driver.set_page_load_timeout(3000)
    # Timeout para scripts asíncronos (por si acaso)
    # driver.set_script_timeout(3000)
    # ⬆⬆⬆ Aumentar timeouts ⬆⬆⬆

    return driver, download_dir

def get_dates():
    
    today = date.today()
    last_day_prev_month = today.replace(day=1) - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)

    return (
        first_day_prev_month.strftime("%Y-%m-%d 00:00"),
        last_day_prev_month.strftime("%Y-%m-%d 23:59")
    )

def log_in(driver, url):
    
    driver.get(url)

    driver.find_element(By.ID, "parameters[username]").send_keys(NEXTBIKE_USER)
    driver.find_element(By.ID, "parameters[password]").send_keys(NEXTBIKE_PASS)
    driver.find_element(By.ID, "login_post").click()

    time.sleep(3)
    
    verification_code = get_code()
    
    driver.find_element(By.ID, "parameters[otp_code]").send_keys(verification_code)
    driver.find_element(By.ID, "login_post").click()                               

def download_from_nextbike(url, driver, download_dir):

    driver.get(url)
    time.sleep(2)

    start_date, end_date = get_dates()

    try:
        driver.find_element(By.ID, "parameters[start_time]").send_keys(start_date)
        driver.find_element(By.ID, "parameters[end_time]").send_keys(end_date)

    except Exception:
        try:
            driver.find_element(By.ID, "parameters[start_date]").send_keys(start_date)
            driver.find_element(By.ID, "parameters[end_date]").send_keys(end_date)

        except Exception: pass

    # Momento justo antes de lanzar la descarga
    start_time = time.time()

    try:
        driver.find_element(By.ID, "parameters[export_csv]").click()
        driver.find_element(By.ID, "queries_view_get").click()
        
    except Exception: pass

    timeout = 60000  # segundos
    file_path = None

    for _ in range(timeout):

        files = glob.glob(os.path.join(download_dir, "*.csv"))

        # Filtrar solo los nuevos (creados/modificados después de start_time)
        new_files = [f for f in files if os.path.getmtime(f) > start_time]

        if new_files:
            # Por si acaso hay más de uno, cogemos el más reciente
            file_path = max(new_files, key=os.path.getmtime)
            break

    return pd.read_csv(file_path, sep='\t', encoding='utf-8')
