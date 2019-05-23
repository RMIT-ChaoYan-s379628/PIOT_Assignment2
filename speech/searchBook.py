import speech_recognition as sr
import MySQLdb, subprocess

HOST = "35.189.34.91"
USER = "root"
PASSWORD = "123456"
DATABASE = "LMS"

MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"

def speechRecognition():
    bookTitle = getBookTitleToSearch()

    if(bookTitle is None):
        print("Failed to get book.")
        return

    print()
    print("Looking for book with title '{}'...".format(bookTitle))
    print()

    rows = searchBookTitle(bookTitle)
    if(rows):
        print("Found:", rows)
    else:
        print("No results found.")

def getBookTitleToSearch():
    # To test searching without the microphone uncomment this line of code
    # return input("Enter the book title to search for: ")

    # Set the device ID of the mic that we specifically want to use to avoid ambiguity
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        if(microphone_name == MIC_NAME):
            device_id = i
            break

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index = device_id) as source:
        # clear console of errors
        subprocess.run("clear")

        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source)

        print("Say the book title to search for.")
        try:
            audio = r.listen(source, timeout = 1.5)
        except sr.WaitTimeoutError:
            return None

    # recognize speech using Google Speech Recognition
    bookTitle = None
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        # bookTitle = r.recognize_google(audio)
        bookTitle = r.recognize_google(audio, key="AIzaSyAPC3pbGKJGjY_FnYpnv71_dR5j1MyszL4")
    except(sr.UnknownValueError, sr.RequestError):
        pass
    finally:
        return bookTitle

def searchBookTitle(bookTitle):
    connection = MySQLdb.connect(HOST, USER, PASSWORD, DATABASE)

    with connection.cursor() as cursor:
        cursor.execute("select * from Book where Title = %s", (bookTitle,))
        rows = cursor.fetchall()

    connection.close()

    return rows

# Execute program.
if __name__ == "__main__":
    speechRecognition()
