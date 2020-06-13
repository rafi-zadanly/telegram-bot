import telebot, mysql.connector, time
from googletrans import Translator

TOKEN = "TOKEN BOT"

myBot = telebot.TeleBot(TOKEN)
myDb = mysql.connector.connect(host='localhost', user='root', database='NAMA DB')
sql = myDb.cursor()

class mybot:
    def __init__(self):
        self.message

    @myBot.message_handler(commands=['start', 'help'])
    def start(message):
        teks = "Halo @"+ message.from_user.username+"\n"
        teks += "/start | untuk menampilkan daftar perintah\n"
        teks += "/speed | untuk cek kecepatan respon bot\n"
        teks += "/tr [kode bahasa] [teks] | untuk menerjemahkan\n"
        teks += "/datasiswa | untuk menampilkan data siswa\n"
        teks += "/creator | untuk menampilkan kontak creator"
        myBot.reply_to(message, teks)

    @myBot.message_handler(commands=['tr'])
    def translate(message):
        sep = message.text.split(" ")
        query = message.text.replace(sep[0] + " ", "")
        sep2 = query.split(" ")
        text = query.replace(sep2[0] + " ", "")
        if query != "/tr":
            result = Translator().translate(text, dest=sep2[0])
            myBot.reply_to(message, result.text)

    @myBot.message_handler(commands=['speed'])
    def speed(message):
        start = time.time()
        myBot.send_message(message.chat.id, "Checking Speed...")
        result = time.time() - start
        myBot.send_message(message.chat.id, str(result) + " Seconds")

    @myBot.message_handler(commands=['creator'])
    def creator(message):
        myBot.send_contact(message.chat.id, "NOMOR HP", "My Creator")

    @myBot.message_handler(commands=['datasiswa'])
    def menu_data_siswa(message):
        query = "select nipd,nama,kelas from tabel_siswa "
        query2 = "select idsiswa from tabel_siswa"
        sql.execute(query)
        data = sql.fetchall()
        sql.execute(query2)
        data2 = sql.fetchall()
        jmldata = sql.rowcount
        kumpuldata = '╔══════════[ Daftar Siswa ]═══════════\n'

        if (jmldata > 0):
            # print(data)
            no = 0
            for x in range(len(data)):
                no += 1
                kumpuldata += "╠[ "+ str(data2[x]) +" ] " + str(data[x]) + "\n"
                kumpuldata = kumpuldata.replace('(', '')
                kumpuldata = kumpuldata.replace(')', '')
                kumpuldata = kumpuldata.replace("'", '')
                kumpuldata = kumpuldata.replace(",", '')
            kumpuldata += "╚══════════[ Total: "+ str(len(data)) +" ]═══════════"
        else:
            print('data kosong')
        myBot.reply_to(message, str(kumpuldata))


print(myDb)
print("-- Bot sedang berjalan --")
myBot.polling(none_stop=True)
