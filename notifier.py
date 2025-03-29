import os
import time
import json
import logging
import smtplib
import sys
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables de entorno
load_dotenv()
SENDER_EMAIL = os.getenv('EMAIL_USER')
SENDER_PASSWORD = os.getenv('EMAIL_PASS')
RECEIVER_EMAIL = os.getenv('EMAIL_RECEIVER')

if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
    logging.error("Faltan variables de entorno en el archivo .env")
    exit(1)

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Modo sin interfaz gráfica
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

URL = "https://hackerone.com/directory/programs?order_direction=DESC&order_field=launched_at"
XPATH_BASE = "/html/body/div[2]/div/div/main/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr[{}]/td[1]/div/div[2]/div[1]/div/span/strong/span/a"

LATEST_PROGRAM_FILE = "latest_program.json"

def load_last_program():
    """Carga el último programa detectado desde un archivo JSON, manejando casos donde el archivo está vacío."""
    if os.path.exists(LATEST_PROGRAM_FILE):
        try:
            # Verificar si el archivo está vacío
            if os.path.getsize(LATEST_PROGRAM_FILE) == 0:
                logging.info("Archivo JSON vacío. Iniciando desde cero.")
                return None
            
            with open(LATEST_PROGRAM_FILE, "r") as f:
                data = json.load(f)
                return data.get("latest_program")
        except json.JSONDecodeError:
            logging.error("El archivo JSON está corrupto o mal formado. Iniciando desde cero.")
            return None
        except Exception as e:
            logging.error(f"Error cargando JSON: {e}")
            return None
    return None

def save_last_program(program_name):
    """Guarda el último programa detectado en un archivo JSON."""
    try:
        with open(LATEST_PROGRAM_FILE, "w") as f:
            json.dump({"latest_program": program_name}, f)
    except Exception as e:
        logging.error(f"Error guardando JSON: {e}")

def send_email(subject, body):
    """Enviar notificación por correo electrónico"""
    try:
        mensaje = EmailMessage()
        mensaje['Subject'] = subject
        mensaje['From'] = SENDER_EMAIL
        mensaje['To'] = RECEIVER_EMAIL
        mensaje.set_content(body, subtype='html')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(mensaje)
            logging.info("Correo de notificación enviado correctamente.")
            #sys.exit(0)  # Terminar el script después de enviar el correo - SOLO ES PARA LOCAL
    except Exception as e:
        logging.error(f"Error enviando correo: {e}")
        #sys.exit(1)  # Terminar el script - error. No se envió el correo - esto solo es PARA LOCAL

logging.info("Iniciando monitoreo de nuevos programas en HackerOne...")
latest_program = load_last_program()

try:
    while True:
        driver.get(URL)
        time.sleep(5)  # Esperar carga de página
        
        try:
            first_program_element = driver.find_element(By.XPATH, XPATH_BASE.format(1))
            first_program_name = first_program_element.text.strip() # obtenemos el nombre del primer programa
            first_program_link = first_program_element.get_attribute("href") # obtenemos el enlace del primer programa
            
            if latest_program is None:
                latest_program = first_program_name
                logging.info(f"Programa actual encontrado: {first_program_name}")
                save_last_program(latest_program)
                send_email(
    "Bug Hunter jf0x0r, primer programa detectado",
    f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto; padding: 20px; background: #f9fafb; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); text-align: center;">
        <h2 style="color: #333; font-size: 24px;">🚀 Primer programa monitoreado</h2>
        <p style="color: #666; font-size: 16px;">Un nuevo programa ha sido registrado en nuestro sistema de monitoreo.</p>
        <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3Z5cm9vNXR0MW51em40OG55eHA2a2VjYm5iZDNxbnZ5eG52YTFibiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/92jYkH87yxV1C/giphy.gif" 
             alt="Mr. Robot feliz" style="width: 100%; max-width: 300px; border-radius: 8px; margin: 10px 0;">
        <div style="background: #fff; padding: 15px; border-radius: 8px; margin: 10px 0; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <p style="margin: 0; font-size: 18px; font-weight: bold; color: #222;">{first_program_name}</p>
        </div>
        <a href="{first_program_link}" style="display: inline-block; text-decoration: none; background: #2563eb; color: white; padding: 10px 15px; border-radius: 6px; font-size: 16px; margin-top: 10px;">🔗 Ver programa en HackerOne</a>
        <p style="color: #aaa; font-size: 12px; margin-top: 15px;">Seguiremos monitoreando nuevos programas para ti.</p>
    </div>
    """
)

            # Si el nombre del primer programa es diferente al último guardado
            elif first_program_name != latest_program:
                logging.info(f"Último programa registrado: {latest_program}")
                latest_program = first_program_name
                save_last_program(latest_program)
                send_email(
    "Bug Hunter jf0x0r, ¡Nuevo programa en HackerOne!",
    f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto; padding: 20px; background: #f9fafb; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); text-align: center;">
        <h2 style="color: #2563eb; font-size: 24px;">🔥 ¡Nuevo programa disponible!</h2>
        <p style="color: #555; font-size: 16px;">Hemos detectado un nuevo programa en HackerOne. ¡No pierdas la oportunidad de revisarlo!</p>
        <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3Z5cm9vNXR0MW51em40OG55eHA2a2VjYm5iZDNxbnZ5eG52YTFibiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/92jYkH87yxV1C/giphy.gif" 
             alt="Mr. Robot feliz" style="width: 100%; max-width: 300px; border-radius: 8px; margin: 10px 0;">
        <div style="background: #fff; padding: 15px; border-radius: 8px; margin: 10px 0; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <p style="margin: 0; font-size: 18px; font-weight: bold; color: #222;">{first_program_name}</p>
        </div>
        <a href="{first_program_link}" style="display: inline-block; text-decoration: none; background: #16a34a; color: white; padding: 12px 18px; border-radius: 6px; font-size: 16px; font-weight: bold; margin-top: 10px;">🚀 Revisar programa</a>
        <p style="color: #aaa; font-size: 12px; margin-top: 15px;">Seguimos monitoreando nuevos programas para ti.</p>
    </div>
    """
)

            else:
                logging.info("No hay nuevos programas.")
                send_email(
    "Bug Hunter jf0x0r, sin novedades",
    f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto; padding: 20px; background: #f9fafb; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); text-align: center;">
        <h2 style="color: #374151; font-size: 22px;">😿 Sin novedades por ahora...</h2>
        <p style="color: #555; font-size: 16px;">Hemos revisado HackerOne, pero no encontramos nuevos programas para ti.</p>
        <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTAxZWZzMHZsNnQyZDd1dmRhbjlsY2R6MThkY3BlM2Y3bXphOWEzZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0K4ovRrRJSs1A4XS/giphy.gif" alt="Gatito triste" style="width: 100%; max-width: 300px; border-radius: 8px; margin: 10px 0;">
        <p style="color: #777; font-size: 14px;">No te preocupes, seguiremos monitoreando y te avisaremos en cuanto haya algo interesante.</p>
        <p style="color: #aaa; font-size: 12px; margin-top: 15px;">🐾 Mientras tanto, relájate y afila tus habilidades de bug hunting. 💻</p>
    </div>
    """
)

        
        except Exception as e:
            logging.error(f"Error al extraer información: {e}")
        
        time.sleep(600)  # Revisar cada 10 minutos

except KeyboardInterrupt:
    logging.info("Script detenido por el usuario.")
    driver.quit()
except Exception as e:
    logging.error(f"Error inesperado: {e}")
    driver.quit()
