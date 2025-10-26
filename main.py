import os
import time
import random
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# ============================================================
# 💡 Dane logowania z Environment Variables (Render)
# ============================================================
PHONE = os.getenv("PHONE")
PASSWORD = os.getenv("PASSWORD")

# ============================================================
# 📋 Wczytywanie list grup i postów (oddzielonych przez ---)
# ============================================================
def load_data():
    """Wczytuje listy grup i postów z plików tekstowych"""
    # Wczytaj grupy (po jednej w linii)
    with open("groups.txt", "r", encoding="utf-8") as g:
        groups = [line.strip() for line in g.readlines() if line.strip()]

    # Wczytaj posty (oddzielone przez ---)
    with open("posts.txt", "r", encoding="utf-8") as p:
        content = p.read()
        posts = [post.strip() for post in content.split('---') if post.strip()]

    return groups, posts

# ============================================================
# ⚙️ Konfiguracja przeglądarki Chrome w środowisku Render
# ============================================================
def create_driver():
    """Tworzy przeglądarkę Chrome w trybie headless na Render"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# ============================================================
# 🔐 Logowanie do Facebooka przez numer telefonu
# ============================================================
def facebook_login(driver):
    """Loguje się do Facebooka przy użyciu numeru telefonu"""
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
# 📝 Publikacja posta w grupie
# ============================================================
def post_to_group(driver, group_url, post_text):
    """Publikuje pojedynczy post w danej grupie"""
    print(f"🚀 Publikuję post w grupie: {group_url}")
    driver.get(group_url)
    time.sleep(random.uniform(4, 6))

    try:
        post_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
        post_box.click()
        time.sleep(random.uniform(2, 4))
        post_box.send_keys(post_text)
        time.sleep(random.uniform(2, 4))

        # Symulacja publikacji (CTRL+ENTER)
        post_box.send_keys(Keys.CONTROL, Keys.ENTER)
        time.sleep(random.uniform(3, 5))
        print("✅ Post opublikowany pomyślnie!\n")
    except Exception as e:
        print(f"❌ Błąd przy publikacji w grupie {group_url}: {e}")

# ============================================================
# 🔁 Główna logika publikacji
# ============================================================
def main():
    """Główna funkcja bota"""
    print("\n============================")
    print("🔄 Rozpoczynam cykl publikacji...")
    print("============================\n")

    groups, posts = load_data()
    driver = create_driver()
    facebook_login(driver)

    for i in range(min(len(groups), len(posts))):
        print(f"➡️  Post {i+1}/{len(posts)}")
        post_to_group(driver, groups[i], posts[i])
        time.sleep(random.uniform(3, 6))

    driver.quit()
    print("\n✅ Wszystkie posty zostały opublikowane!\n")

# ============================================================
# ⏰ Harmonogram - powtarzaj co 2 godziny
# ============================================================
schedule.every(2).hours.do(main)

# Uruchom pierwszy cykl od razu
main()

# Pętla działania (Render utrzymuje proces w tle)
while True:
    schedule.run_pending()
    time.sleep(10)
