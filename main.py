import os
import time
import random
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

# ============================================================
# 💡 Załaduj dane logowania z pliku .env
# ============================================================
load_dotenv()
PHONE = os.getenv("PHONE")      # numer telefonu do logowania
PASSWORD = os.getenv("PASSWORD")  # hasło do konta

# ============================================================
# 📋 Wczytaj listy grup i postów (z separatorami ---)
# ============================================================
def load_data():
    """Wczytuje listy grup i postów z plików tekstowych"""
    # wczytaj grupy
    with open("groups.txt", "r", encoding="utf-8") as g:
        groups = [line.strip() for line in g.readlines() if line.strip()]

    # wczytaj posty – każdy blok oddzielony przez ---
    with open("posts.txt", "r", encoding="utf-8") as p:
        content = p.read()
        posts = [post.strip() for post in content.split('---') if post.strip()]

    return groups, posts

# ============================================================
# ⚙️ Konfiguracja przeglądarki Chrome w trybie headless
# ============================================================
def create_driver():
    """Tworzy przeglądarkę Chrome w trybie headless (bez GUI)"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # tryb bez GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# ============================================================
# 🔐 Logowanie do Facebooka za pomocą numeru telefonu
# ============================================================
def facebook_login(driver):
    """Loguje się na Facebooka przy użyciu numeru telefonu"""
    driver.get("https://www.facebook.com/login")
    time.sleep(random.uniform(3, 5))

    try:
        phone_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "pass")
        login_button = driver.find_element(By.NAME, "login")

        phone_input.send_keys(PHONE)
        time.sleep(random.uniform(1, 2))
        password_input.send_keys(PASSWORD)
        time.sleep(random.uniform(1, 3))
        login_button.click()

        time.sleep(random.uniform(5, 7))
        print("✅ Zalogowano na Facebooka (numer telefonu).")
    except Exception as e:
        print(f"❌ Błąd podczas logowania: {e}")

# ============================================================
# 📝 Publikacja posta w danej grupie
# ============================================================
def post_to_group(driver, group_url, post_text):
    """Publikuje pojedynczy post w danej grupie"""
    print(f"🚀 Publikuję post w grupie: {group_url}")
    driver.get(group_url)
    time.sleep(random.uniform(4, 6))

    try:
        # Znajdź pole do wpisania posta (Facebook często zmienia selektory)
        post_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
        post_box.click()
        time.sleep(random.uniform(2, 4))
        post_box.send_keys(post_text)
        time.sleep(random.uniform(2, 4))

        # Symuluj kliknięcie Enter (lub kombinację CTRL+Enter)
        post_box.send_keys(Keys.CONTROL, Keys.ENTER)
        time.sleep(random.uniform(3, 5))
        print("✅ Post opublikowany pomyślnie!\n")
    except Exception as e:
        print(f"❌ Błąd przy publikacji w grupie {group_url}: {e}")

# ============================================================
# 🔁 Główna logika publikacji
# ============================================================
def main():
    """Główna funkcja cyklu publikacji"""
    print("\n============================")
    print("🔄 Rozpoczynam cykl publikacji...")
    print("============================\n")

    groups, posts = load_data()
    driver = create_driver()
    facebook_login(driver)

    # Dopasuj posty do grup 1:1
    for i in range(min(len(groups), len(posts))):
        print(f"➡️  Post {i+1}/{len(posts)}")
        post_to_group(driver, groups[i], posts[i])
        time.sleep(random.uniform(3, 6))  # realistyczne opóźnienia

    driver.quit()
    print("\n✅ Wszystkie posty zostały opublikowane!\n")

# ============================================================
# ⏰ Harmonogram - powtarzaj co 2 godziny
# ============================================================
schedule.every(2).hours.do(main)

# Uruchom pierwszy raz od razu
main()

# Pętla działania (ciągła praca bota)
while True:
    schedule.run_pending()
    time.sleep(10)
