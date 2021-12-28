import speech_recognition as sr
import sys
import subprocess
from pymongo import MongoClient

# TEST
filename = "king.wav"
hebrew = True
ffmpegPath = "C:\\Users\\Oratl\\Documents\\path\\ffmpeg.exec"
# filename = sys.argv[1]
# language = sys.argv[2]
# ffmpegPath = sys.argv[3]
# if language == "Hebrew":
#     hebrew = True
# else:
#     hebrew = False
renew = False
if renew:
    command = ffmpegPath + " -i " + filename + ".mp4 -ab 160k -ac 2 -ar 44100 -vn .\\" + filename + ".wav"
    subprocess.call(command, shell=True)

r = sr.Recognizer()
# TEST
# filename = filename + ".wav"

def send_data_to_mongo(wordInPart, timestamp, video_name):
    # load data
    textfile = 'tarnscript.txt'
    file = open(textfile, 'w', encoding="utf8")
    file.truncate(0)
    file.write(wordInPart)
    file.close()
    file = open(textfile, 'rt', encoding="utf8")
    text = file.read()
    file.close()
    # split into words
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('hebrew'))
    words = [w for w in words if not w in stop_words]
    print(words[:10])
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["infomotion"]
    collection = db["words"]
    list1 = [{"name": i, "stream_name": video_name, "part": timestamp} for i in words[:10]]
    # Inseting the entire list in the collection
    collection.insert_many(list1)


try:
    with sr.AudioFile(filename) as source:
        video_duration = int(source.DURATION)
        for x in range(0, video_duration, 60):
            minute_offset: int = x
            minute_duration: int = x + 60
            # TEST
            # audio_data = r.record(source, offset=minute_offset, duration=minute_duration)
            if hebrew:
                # TEST
                text = "אין צדק בחיים נכון ידידי הקטן בזמן שחלק נולדו לחגוג אחרים מעבירים את חייהם בחשיכה מתחננים בלי שאריות מדיסני כל מה שאתה רואה מתקיים בשיווי משקל עדין עם הבמאי של ספר הג׳ונגל בזמן שאחרים מחפשים מה הם יכולים לקחת מלאך אמיתי מחפש מה הוא יכול לתת הקיץ ברח מסיבה או לעולם אל תחזור אלי אתה חייב לחזור למקומך גלגל החיים מלך האריות"
                # text = r.recognize_google(audio_data, language='he-he', show_all=True)
            else:
                # TEST
                text = "אין צדק בחיים נכון ידידי הקטן בזמן שחלק נולדו לחגוג אחרים מעבירים את חייהם בחשיכה מתחננים בלי שאריות מדיסני כל מה שאתה רואה מתקיים בשיווי משקל עדין עם הבמאי של ספר הג׳ונגל בזמן שאחרים מחפשים מה הם יכולים לקחת מלאך אמיתי מחפש מה הוא יכול לתת הקיץ ברח מסיבה או לעולם אל תחזור אלי אתה חייב לחזור למקומך גלגל החיים מלך האריות"
                # text = r.recognize_google(audio_data, show_all=True)
            if minute_offset == 0:
                temp1 = int((minute_duration / 60) + 1)
                temp1 = str(temp1)
                time = "0 - " + temp1
            else:
                temp1 = int((minute_offset / 60))
                temp1 = str(temp1)
                temp2 = int((minute_duration / 60) + 1)
                temp2 = str(temp2)
                time = temp1 + " - " + temp2
            # TEST
            send_data_to_mongo(text, time, filename)
            # send_data_to_mongo(text['alternative'][0]['transcript'], time, filename)
except Exception as e:
    print(e)
