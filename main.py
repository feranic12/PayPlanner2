import PySimpleGUI as psg
import db


def main():
    db_driver = db.DB("pay_planner2_db.db")
    table_data = db_driver.get_subs_for_table()
    new_table_data = []
    for row in range(len(table_data)):
        row_list = []
        for col in range(len(table_data[row])):
            if col != 2:
                new_cell = table_data[row][col]
            else:
                new_cell = str(table_data[row][col]) + " мес."
            row_list.append(new_cell)
            tup = tuple(row_list)
        new_table_data.append(tup)
    table_data = new_table_data

    header_list = ["Название сервиса", "Состояние подписки",
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
            states_list = []
            duration_list = []
            durations_from_db = db_driver.get_all_durations()
            states_from_db = db_driver.get_all_states()
            for st in range(0, len(states_from_db)):
                states_list.append(str(states_from_db[st][0]))
            for dur in range(0, len(durations_from_db)):
                duration_list.append(str(durations_from_db[dur][0]))
            layout2 = [[psg.Text("Название подписки:"), psg.Input(key="_subscription_")],
                       [psg.Text("Статус:"), psg.Combo(states_list, default_value=states_list[0], key="_state_"),
                        psg.Text("Срок продления:"), psg.Combo(duration_list, default_value=duration_list[0], key="_duration_"),
                       psg.Text("мес.")],
                         [psg.Text("Сумма списания:"), psg.Input(key="_price_")],
                        [psg.Text("Срок окончания:"), psg.Input(key="_ending_"),
                          psg.CalendarButton("Выбрать дату", target="_ending_", key="_termend_", format="%d-%m-%Y")],
                          [psg.Button("Сохранить")]]
            window2 = psg.Window("Добавление подписки", layout2)
            while True:
                event, values = window2.read()
                if event in (None, 'Exit'):
                    break
                if event == "Сохранить":
                    service_name = values["_subscription_"]
                    state_id = db_driver.get_id_from_state(values["_state_"])
                    duration_id = db_driver.get_id_from_duration(values["_duration_"])
                    term_end = values["_ending_"]
                    price = values["_price_"]
                    tuple_to_add = (service_name, state_id, duration_id, price, term_end)
                    db_driver.add_subscription_to_db(tuple_to_add)
                window2.close()
    window.close()


if __name__=="__main__":
    main()