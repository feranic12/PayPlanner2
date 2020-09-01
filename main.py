import PySimpleGUI as psg
import db


def main():
    db_driver = db.DB("pay_planner2_db.db")
    table_data = db_driver.get_subs_for_table()
    new_table_data = []
    for row in range(len(table_data)):
        row_list = []
        for col in range(len(table_data[row])):
            if col != 5:
                new_cell = table_data[row][col]
            else:
                new_cell = str(table_data[row][col]) + " мес."
            row_list.append(new_cell)
            tup = tuple(row_list)
        new_table_data.append(tup)
    table_data = new_table_data

    header_list = ["Название сервиса", "Состояние подписки", "Банк карты", "Платежная система", "Номер карты",
                   "Период продления","Сумма", "Срок окончания"]
    my_table = psg.Table(values = table_data,
                headings=header_list,
               justification="left", bind_return_key=True, key="_table_")
    layout = [[my_table],
        [psg.Button("Добавить")]
    ]
    window = psg.Window('Главное окно', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == "_table_":
            layout1 = [[psg.Ok()]]
            window1 = psg.Window("Окно 1", layout1)
            while True:
                event, values = window1.read()
                if event in (None, 'Ok'):
                    break
            window1.close()
        if event == "Добавить":
            layout2 = [[psg.Ok()]]
    window.close()


if __name__=="__main__":
    main()