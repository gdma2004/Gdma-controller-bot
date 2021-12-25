#####################################################################################################
#   _____     _                    _____            _             _ _             ____        _     #
#  / ____|   | |                  / ____|          | |           | | |           |  _ \      | |    #
# | |  __  __| |_ __ ___   __ _  | |     ___  _ __ | |_ _ __ ___ | | | ___ _ __  | |_) | ___ | |_   #
# | | |_ |/ _` | '_ ` _ \ / _` | | |    / _ \| '_ \| __| '__/ _ \| | |/ _ \ '__| |  _ < / _ \| __|  #
# | |__| | (_| | | | | | | (_| | | |___| (_) | | | | |_| | | (_) | | |  __/ |    | |_) | (_) | |_   #
#  \_____|\__,_|_| |_| |_|\__,_|  \_____\___/|_| |_|\__|_|  \___/|_|_|\___|_|    |____/ \___/ \__|  #
#                                                                                                   #
#####################################################################################################                                                                                                 



# Feito por Gabriel Dantas
# https://github.com/gdma2004

# ChatBot de comunicação remota com o computador
# Altere os ids de usuário para que você possa usar





# Módulos
import telebot, psutil, time, os, subprocess
from threading import Thread
from telebot import types
from logging import exception



# Bot Token
bot = telebot.TeleBot('BOTE_SEU_TOKEN_AQUI')

# Admin User ID
admin_id = BOTE_SEU_ID_AQUI

# Home
home = os.getenv('HOME')

# Avisar para os usuários
bot.send_message(admin_id, 'Bot iniciado')




# Variáveis de informações do sistema
def system():

    global batt, cpu, temperature, uptime, memory_mib

    while True:
        def temp():
            tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
            cpu_temp = tempFile.read()
            tempFile.close()
            return round(float(cpu_temp)/1000, 2)
        def upt():
            result = int((time.time() - psutil.boot_time())/60)
            return result

        batt = int(psutil.sensors_battery().percent)
        cpu = int(psutil.cpu_percent())
        memory_mib = int((psutil.virtual_memory().used)/1000000)
        temperature = temp()
        uptime = upt()
        time.sleep(2)



def comandos():
    
    # Comando start (exibe o menu e inicia o bot)
    @bot.message_handler(commands=['start'])
    def start(message):

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
        markup.add('/start','/status','/voice','/audiolocal','/screenshot','/webcam','/command','/lock','/unlock','/desligar')

        if message.chat.id == admin_id:
            bot.send_message(message.chat.id, '🎈 Olá novamente!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')
            bot.send_message(admin_id, 'Há uma pessoa tentando usar o bot: {} {}'.format(message.chat.first_name, message.chat.last_name))



    # Comando deligar (desliga o computador)
    @bot.message_handler(commands=['desligar'])
    def desligar(message):

        if message.chat.id == admin_id:
            for i in range(3):
                bot.send_message(message.chat.id, '🎈 Desligando em {}'.format(3-i))
                time.sleep(1)
            bot.send_message(message.chat.id, '🎈 Computador desligado. Ligue-o para que eu possa ajudá-lo.')
            os.system('poweroff')
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')
    


    # Comando voice (roda um comando de voz)
    class User_voice:
        def __init__(self, voice):
            self.vc = voice

    @bot.message_handler(commands=['voice'])
    def voice(message):

        if message.chat.id == admin_id:
            audio_message = bot.reply_to(message, '🎈 Digite o que você quer falar')
            bot.register_next_step_handler(audio_message, processo_audio)
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')


    def processo_audio(message):

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
        markup.add('/start','/status','/voice','/audiolocal','/screenshot','/webcam','/command','/lock','/unlock','/desligar')
        comando_de_voz = message.text
        input_comando_voz = User_voice.vc = str(comando_de_voz)
        os.system('espeak -vpt-BR+f4 -s170 "{}"'.format(input_comando_voz))
        bot.send_message(message.chat.id,'🎈 Comando de áudio enviado', reply_markup=markup)



    # Comando screenshot (tira print do sistema e envia ao usuário)
    @bot.message_handler(commands=['screenshot'])
    def screenshot(message):

        if message.chat.id == admin_id:
            os.system("cd ~/ && maim print.png")
            bot.send_photo(message.chat.id, photo=open(home+'/print.png', 'rb'))
            os.system('rm ~/print*.png')
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')



    # Comando audiolocal (envia áudio com som ambiente)
    class User_audio_local:
        def __init__(self, audio_local):
            self.al = audio_local

    @bot.message_handler(commands=['audiolocal'])
    def audiolocal(message):
        if message.chat.id == admin_id:
            time_audio = bot.reply_to(message, '🎈 Digite o tempo de gravação desejado em segundos.')
            bot.register_next_step_handler(time_audio, processo_audio_local)
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')


    def processo_audio_local(message):

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
        markup.add('/start','/status','/voice','/audiolocal','/screenshot','/webcam','/command','/lock','/unlock','/desligar')
        al = message.text
        input_comando_audiolocal = User_audio_local.al = al
        
        try: 
            int(input_comando_audiolocal) 
            bot.send_message(message.chat.id,'🎈 Gravando áudio de {} segundos'.format(input_comando_audiolocal))
            os.system('arecord -d {} -f U8 ~/audiolocal.mp3'.format(input_comando_audiolocal))
            bot.send_audio(message.chat.id, audio = open(home+'/audiolocal.mp3', 'rb'), reply_markup=markup)
            os.system('rm ~/audiolocal*.mp3')
        except Exception as e:
            bot.send_message(message.chat.id, '🎈 Digite um valor válido.', reply_markup=markup)
        



    # Comando lock (bloqueia o sistema - i3lock)
    @bot.message_handler(commands=['lock'])
    def lock(message):

        if message.chat.id == admin_id:
            bot.send_message(message.chat.id, '🎈 Tela bloqueada.')
            os.system('i3lock -c 000000')
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')
    


    # Comando unlock (desbloqueia o sistema - i3lock)
    @bot.message_handler(commands=['unlock'])
    def unlock(message):
        
        if message.chat.id == admin_id:
            bot.send_message(message.chat.id, '🎈 Tela desbloqueada.')
            os.system('pkill -f i3lock')
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')



    # Comando command (executa um comando de terminal no sistema)
    class User:
        def __init__(self, command):
            self.cmd = command

    @bot.message_handler(commands=['command'])
    def command(message):

        if message.chat.id == admin_id:
            msg = bot.reply_to(message, '🎈 Digite o comando desejado')
            bot.register_next_step_handler(msg, processo)
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')


    def processo(message):

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
        markup.add('/start','/status','/voice','/audiolocal','/screenshot','/webcam','/command','/lock','/unlock','/desligar')
        cmd = message.text
        input_comando = User.cmd = str(cmd)

        try:
            exit = subprocess.Popen(input_comando, shell=True, stdout=subprocess.PIPE)
            subprocess_return = exit.stdout.read()
            bot.send_message(message.chat.id, subprocess_return, reply_markup=markup)
        except Exception as e:
            bot.send_message(message.chat.id, '🎈 O comando foi executado, porém não há output disponível para exibir', reply_markup=markup)



    # Comando status (indica informações em tempo real do sistema)
    @bot.message_handler(commands=['status'])
    def status(message):

        if message.chat.id == admin_id:
            bot.send_message(message.chat.id, '🎈 STATUS DO SISTEMA\n\n\n⚙️ CPU: {}%\n\n📊 RAM: {} MiB\n\n🔋 BAT: {}%\n\n🌡️ TEMP: {}°C\n\n⏰ UPTIME: {} min'.format(cpu, memory_mib, batt, temperature, uptime))
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')
    
    

    # Comando webcam (envia uma foto tirada por meio da webcam em tempo real)
    @bot.message_handler(commands=['webcam'])
    def webcam(message):

        if message.chat.id == admin_id:
            os.system('cd ~/ && ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 webcam.jpeg')
            bot.send_photo(message.chat.id, photo=open(home+'/webcam.jpeg', 'rb'))
            os.system('rm ~/webcam*.jpeg')
        else:
            bot.send_message(message.chat.id, 'Você não é um deles 😎🤭')



# Threads de inicialização paralela    
Thread(target = system).start()
Thread(target = comandos).start()



# Looping
bot.polling()
