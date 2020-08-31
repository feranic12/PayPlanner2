import PySimpleGUI
import db


def main():
    db_driver = db.DB("pay_planner2_db.db")
    table_data = db_driver.get_subs_for_table()
    header_list = ["Название сервиса", "Состояние подписки", "Банк карты", "Платежная система", "Номер карты",
                   "Период продления","Сумма", "Срок окончания"]
    my_table = PySimpleGUI.Table(values = table_data,
                headings=header_list,
               justification="left", bind_return_key=True, key="_table_")
    layout = [[my_table],
        [PySimpleGUI.Button("Добавить")]
    ]
    window = PySimpleGUI.Window('Главное окно', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit', 'Cancel'):
            break
        if event in ("_table_", "Добавить"):
            layout1 = [[PySimpleGUI.Ok()]]
            window1 = PySimpleGUI.Window("Окно 1", layout1)
            while True:
                event, values = window1.read()
                if event in (None, 'Ok'):
                    break
            window1.close()
    window.close()


if __name__=="__main__":
    main()