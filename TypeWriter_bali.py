from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from pynput.keyboard import Controller
from colorama import init, Fore
from selenium.webdriver.common.action_chains import ActionChains

# Initialisiere colorama
init(autoreset=True)

# Funktion zum Anzeigen des Logos
def print_logo():
    logo = r"""
     ____    __    __    ____ 
    (  _ \  /__\  (  )  (_  _)
     ) _ < /(__)\  )(__  _)(_
    (____/(__)(__)(____)(____)
    """
    print(Fore.GREEN + logo)
    print(Fore.LIGHTMAGENTA_EX + "Made by bali\n")
    print(Fore.LIGHTMAGENTA_EX + "AKA Alex\n")

# Initialisiere den Tastaturcontroller
keyboard = Controller()

# Logo anzeigen
print_logo()

# Benutzerdaten über die Eingabeaufforderung abfragen
username = input("Username: ")
password = input("Password: ")
print()

# Zeitspanne für das Tippen abfragen
delay = float(input("Time in Seconds for 1 Word: "))

# Chrome WebDriver im aktuellen Verzeichnis einrichten
current_dir = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = os.path.join(current_dir, 'chromedriver.exe')  # Oder 'chromedriver' ohne .exe auf Linux

# Chrome WebDriver initialisieren
driver = webdriver.Chrome(executable_path=chrome_driver_path)

try:
    # Website öffnen
    driver.get("https://at4.typewriter.at/index.php")

    # Warten, bis die Seite vollständig geladen ist
    time.sleep(2)

    # Einwilligen-Button klicken
    einwilligen_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[1]/div[2]/div[2]/button[1]/p')
    einwilligen_button.click()

    # Warten, bis die nächste Seite geladen ist
    time.sleep(2)

    # Benutzername eingeben
    username_input = driver.find_element(By.XPATH, '//*[@id="LoginForm_username"]')
    username_input.send_keys(username)

    # Passwort eingeben
    password_input = driver.find_element(By.XPATH, '//*[@id="LoginForm_pw"]')
    password_input.send_keys(password)

    # Login-Button klicken
    login_button = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input')
    login_button.click()

    # Warten, bis die nächste Seite geladen ist
    time.sleep(5)

    # Lektion starten
    lektion_button = driver.find_element(By.XPATH, '//*[@id="contentBody"]/div[2]/div[1]/a')
    lektion_button.click()

    # Warten, bis der Start-Button sichtbar ist und klicken
    start_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div[3]/div/button')))
    start_button.click()

    # Warten, bis der Text geladen ist
    text_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div[3]/div[2]/div[2]')))
    
    # Den gesamten Text aus dem Textfeld auslesen
    todo_text = text_field.text.strip()

    if not todo_text:
        print("Kein Text zum Tippen gefunden.")
        driver.quit()
        exit()

    print("Text zum Tippen:", todo_text)  # Debugging-Zeile

    # Warten, bis das Eingabefeld für das Tippen verfügbar ist
    input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div[3]/div[2]/div[2]')))

    # Das Element ins Blickfeld scrollen
    driver.execute_script("arguments[0].scrollIntoView();", input_field)

    # Aktiviere das Eingabefeld
    actions = ActionChains(driver)
    actions.move_to_element(input_field).click().perform()

    time.sleep(0.5)  # Kurze Pause, um sicherzustellen, dass der Klick verarbeitet wird

    # Text tippen, Buchstabe für Buchstabe
    for character in todo_text:
        keyboard.press(character)
        keyboard.release(character)
        print(f"Taste gedrückt: {character}")  # Debugging-Ausgabe
        time.sleep(delay)  # Verwende die manuell eingestellte Zeitspanne

except Exception as e:
    print("Ein Fehler ist aufgetreten:", e)

# Zum Schluss soll das Fenster offen bleiben
input("Drücke Enter, um das Programm zu beenden...")

# Browser schließen

