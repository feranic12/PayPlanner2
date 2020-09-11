import PySimpleGUI as psg
import db
from util import Util


def main():
    db_driver = db.DB("pay_planner2_db.db")
    table_data = Util.make_basic_table(db_driver)
    header_list = ["Название сервиса", "Состояние подписки",
                   "Период продления","Сумма", "Срок окончания"]
    my_table = psg.Table(values = table_data,
                headings=header_list,
               justification="left", bind_return_key=True, key="_table_")
    layout = [[my_table],
        [psg.Button("Добавить", key="_addbutton_"), psg.Button("Редактировать", key="_editbutton_"),
         psg.Button("Удалить", key="_deletebutton_")]
    ]
    window = psg.Window('Главное окно', layout)

    while True:
        event, values = window.read(timeout=100)
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
        if event == "_addbutton_":
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
                        [psg.Text("Срок окончания:"), psg.Input(disabled=True, key="_ending_"),
                         # psg.CalendarButton("Выбрать дату", target="_ending_", key="_termend_", format="%Y-%m-%d")],
                         psg.Button("Выбрать дату", key="_termend_")],
                          [psg.Button("Сохранить")]]
            window2 = psg.Window("Добавление подписки", layout2)
            while True:
                event, values = window2.read(timeout=100)
                if event in (None, 'Exit'):
                    break
                if event == "_termend_":
                    date = psg.popup_get_date()
                    month = "0" + str(date[0]) if len(str(date[0])) == 1 else str(date[0])
                    day = "0" + str(date[1]) if len(str(date[1])) == 1 else str(date[1])
                    year = str(date[2])
                    date_in_format = year + "-" + month + "-" + day
                    window2["_ending_"](date_in_format)
                if event == "Сохранить":
                    if (values["_subscription_"] == "") or \
                    (values["_price_"] == "") or \
                    (values["_ending_"] == ""):
                        psg.Popup("Ошибка", "Заполните все поля формы.")
                        continue

                    service_name = values["_subscription_"]
                    state_id = db_driver.get_id_from_state(values["_state_"])
                    duration_id = db_driver.get_id_from_duration(values["_duration_"])
                    term_end = values["_ending_"]
                    price = values["_price_"]
                    tuple_to_add = (service_name, state_id, duration_id, price, term_end)
                    db_driver.add_subscription_to_db(tuple_to_add)
                    psg.Popup("Добавление", "Новая подписка успешно добавлена!")
                    window["_table_"](Util.make_basic_table(db_driver))
            window2.close()
        if event == "_deletebutton_":
            if len(values["_table_"]) == 0:
                psg.Popup("Ошибка", "Не выбрана запись для удаления")
                continue
            row_number = values["_table_"][0]
            table_data = Util.make_basic_table(db_driver)
            service_name_to_delete = table_data[row_number][0]
            id_to_delete = db_driver.get_sub_id_by_name(service_name_to_delete)
            db_driver.delete_sub(id_to_delete)
            psg.Popup("Удаление", "Выбранная подписка успешно удалена!")
            window["_table_"](Util.make_basic_table(db_driver))
    window.close()


if __name__=="__main__":
    main()