#Refactorización del código para notificar nuevos programas en HackerOne a través de Telegram. - El puto email se jodió
# By jf0x0r
# Date: 2025-12-25

import os
import json
import logging
import requests
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Cargar variables de entorno
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    logging.error("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en el archivo .env")
    exit(1)

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Modo sin interfaz gráfica
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

URL = "https://hackerone.com/directory/programs?order_direction=DESC&order_field=launched_at"
XPATH_BASE = "/html/body/div[2]/div/div/main/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr[{}]/td[1]/div/div[2]/div[1]/div/span/strong/span/a"

LATEST_PROGRAM_FILE = "latest_program.json"


def load_last_program():
    """Carga el último programa detectado desde un archivo JSON."""
    if os.path.exists(LATEST_PROGRAM_FILE):
        try:
            with open(LATEST_PROGRAM_FILE, "r") as f:
                data = json.load(f)
                return data.get("latest_program")
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    return None


def save_last_program(program_name):
    """Guarda el último programa detectado en un archivo JSON."""
    if program_name and program_name.strip():
        with open(LATEST_PROGRAM_FILE, "w") as f:
            json.dump({"latest_program": program_name.strip()}, f)
    else:
        logging.warning("Intento de guardar un nombre de programa vacío. Se omite.")


def send_telegram_message(title, caption_html, image_url=None):
    bot_token = TELEGRAM_BOT_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    if image_url:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        payload = {
            "chat_id": chat_id,
            "photo": image_url,
            "caption": caption_html,
            "parse_mode": "HTML"
        }
    else:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": caption_html,
            "parse_mode": "HTML"
        }

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"[!] Error enviando mensaje: {response.text}")

# Ejecutar monitoreo
try:
    driver.get(URL)
    #time.sleep(5)  # Esperar carga de página
    driver.implicitly_wait(10)

    try:
        first_program_element = driver.find_element(By.XPATH, XPATH_BASE.format(1))
        first_program_name = first_program_element.text.strip()
        first_program_link = first_program_element.get_attribute("href")

        if not first_program_name:
            logging.warning("No se pudo obtener el nombre del primer programa. Puede que el sitio no cargó bien.")
            # Puedes reintentar una vez más aquí antes de salir
            driver.implicitly_wait(5)
            first_program_element = driver.find_element(By.XPATH, XPATH_BASE.format(1))
            first_program_name = first_program_element.text.strip()
            first_program_link = first_program_element.get_attribute("href")

        if not first_program_name:
            logging.error("Segundo intento fallido. No se pudo obtener el nombre del programa. Abortando.")
            sys.exit(1)  # Aquí puedes poner 1 para indicar error real

        latest_program = load_last_program()

        if not latest_program or latest_program.strip() == "":
            # Solo lo tratamos como primer monitoreo si el archivo no tiene nada válido
            logging.info(f"Primer monitoreo, guardando programa: {first_program_name}")
            save_last_program(first_program_name)
            send_telegram_message(
            "Bug Hunter jf0x0r, primer programa detectado",
            f"""
            <b>🚀 Primer programa monitoreado</b>
            Un nuevo programa ha sido registrado en el sistema de monitoreo Felipe.

            <b>{first_program_name}</b>
            🔗 <a href="{first_program_link}">Ver programa en HackerOne</a>

            <i>Seguiré monitoreando nuevos programas para ti.</i>
            """,
            image_url="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3Z5cm9vNXR0MW51em40OG55eHA2a2VjYm5iZDNxbnZ5eG52YTFibiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/92jYkH87yxV1C/giphy.gif"
            )

        elif first_program_name != latest_program:
            if not first_program_name:
                logging.warning("Intento de guardar un nombre de programa vacío. Se omite.")
            else:
                logging.info(f"Nuevo programa encontrado: {first_program_name}")
                save_last_program(first_program_name)
                send_telegram_message(
                "Bug Hunter jf0x0r, ¡Nuevo programa en HackerOne!",
                f"""
            <b>🔥 ¡Nuevo programa disponible!</b>
            <b>{first_program_name}</b>

            🚀 <a href="{first_program_link}">Revisar programa en HackerOne</a>

            <i>Seguiré monitoreando nuevos programas para ti, Felipe.</i>
            """,
                image_url="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3Z5cm9vNXR0MW51em40OG55eHA2a2VjYm5iZDNxbnZ5eG52YTFibiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/92jYkH87yxV1C/giphy.gif"
    )
        else:
            logging.info("No hay nuevos programas.")
            send_telegram_message(
            "Bug Hunter jf0x0r, sin novedades",
            """
        <b>😿 Sin novedades por ahora...</b>
        <i>No encuentro nuevos programas por el momento.</i>

        Relájate y siguele dando duro al Hacking. 💻
        """,
            image_url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTAxZWZzMHZsNnQyZDd1dmRhbjlsY2R6MThkY3BlM2Y3bXphOWEzZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0K4ovRrRJSs1A4XS/giphy.gif"
)

    except Exception as e:
        logging.error(f"Error al extraer información: {e}")

finally:
    driver.quit()  # Cerrar el driver correctamente
