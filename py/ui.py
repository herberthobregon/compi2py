import eel

eel.init("web/dist")

@eel.expose
def save_data():
    print('intentaaaa')
    data = get_editor_txt()
    print('info:',data)

def set_editor_txt(txt: str):
    eel.setEditorText(txt)

def get_editor_txt():
    return eel.getEditorText()

def start():
    eel.start("index.html")
