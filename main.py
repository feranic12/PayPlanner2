import PySimpleGUI
import db


def main():
    layout = [
        [PySimpleGUI.Button("Добавить")],
         [PySimpleGUI.Ok(), PySimpleGUI.Cancel()]
    ]
    layout1 = [[PySimpleGUI.Ok()]]
    window = PySimpleGUI.Window('Главное окно', layout)
    db_driver = db.DB("pay_planner2_db.db")
    while True:
        event, values = window.read()
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == "Добавить":
            window1 = PySimpleGUI.Window("Окно 1", layout1)
            while True:
                event, values = window1.read()
                if event in (None, 'Ok'):
                    break
            window1.close()
    window.close()


if __name__=="__main__":
    main()