import PySimpleGUI
import db


def main():
    layout = [
        [PySimpleGUI.Ok()]
    ]
    window = PySimpleGUI.Window('Главное окно', layout).read()


if __name__=="__main__":
    main()