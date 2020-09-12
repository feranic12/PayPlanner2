import PySimpleGUI as psg
import db
import util


def main():
    db_driver = db.DB("pay_planner2_db.db")
    notifier = util.Notifier(db_driver)
    notifier.check_updates(db_driver)
    table_data = util.TableMaker.make_basic_table(db_driver)
    layout1_maker = util.Layout1Maker(db_driver)
    layout2_maker = util.Layout2Maker(db_driver)
    header_list = ["Название сервиса", "Состояние подписки",
                   "Период продления","Сумма", "Срок окончания"]
    my_table = psg.Table(values = table_data,
                headings=header_list,
               justification="left", bind_return_key=True, key="_table_")
    layout = [[my_table],
        [psg.Button("Добавить", key="_addbutton_"), psg.Button("Редактировать", key="_editbutton_"),
         psg.Button("Удалить", key="_deletebutton_"), psg.Button("Проверить", key="_checkbutton_")]
    ]
    window = psg.Window('Главное окно', layout)

    while True:
        event, values = window.read(timeout=100)
        if event in (None, "Exit", "Cancel"):
            break
        if event == "_addbutton_":
            layout1 = layout1_maker.make_layout1(db_driver)
            window1 = psg.Window("Добавление подписки", layout1)
            while True:
                event, values = window1.read(timeout=100)
                if event in (None, "Exit"):
                    break
                if event == "_termend_":
                    date = psg.popup_get_date()
                    if date is None:
                        continue
                    month = "0" + str(date[0]) if len(str(date[0])) == 1 else str(date[0])
                    day = "0" + str(date[1]) if len(str(date[1])) == 1 else str(date[1])
                    year = str(date[2])
                    date_in_format = year + "-" + month + "-" + day
                    window1["_ending_"](date_in_format)
                if event == "_savebutton_":
                    if (values["_subscription_"] == "") or \
                    (values["_price_"] == "") or \
                    (values["_ending_"] == ""):
                        psg.Popup("Ошибка", "Заполните все поля формы.")
                        continue
                    service_name = values["_subscription_"]
                    state_id = db_driver.get_id_by_state(values["_state_"])
                    duration_id = db_driver.get_id_by_duration(values["_duration_"])
                    price = values["_price_"]
                    term_end = values["_ending_"]
                    tuple_to_add = (service_name, state_id, duration_id, price, term_end)
                    db_driver.add_subscription_to_db(tuple_to_add)
                    psg.Popup("Добавление", "Новая подписка успешно добавлена!")
                    window["_table_"](util.TableMaker.make_basic_table(db_driver))
            window1.close()
            
        if event == "_editbutton_" or event == "_table_":
            if len(values["_table_"]) == 0:
                psg.Popup("Ошибка", "Не выбрана запись для редактирования")
                continue
            row_number = values["_table_"][0]
            table_data = util.TableMaker.make_basic_table(db_driver)
            service_name = table_data[row_number][0]
            id_to_update = db_driver.get_sub_id_by_name(service_name)
            state_id = db_driver.get_id_by_state(table_data[row_number][1])
            duration_raw = table_data[row_number][2]
            duration = duration_raw[0:-5]
            duration_id = db_driver.get_id_by_duration(duration)
            price = table_data[row_number][3]
            term_end = table_data[row_number][4]
            tuple_to_update = (id_to_update, service_name, state_id, duration_id, price, term_end)
            layout2 = layout2_maker.make_layout2(tuple_to_update)
            window2 = psg.Window("Редактирование подписки", layout2)
            while True:
                event, values = window2.read()
                if event in (None, "Exit", "Cancel"):
                    break
                if event == "_termend_":
                    date = psg.popup_get_date()
                    if date is None:
                        continue
                    month = "0" + str(date[0]) if len(str(date[0])) == 1 else str(date[0])
                    day = "0" + str(date[1]) if len(str(date[1])) == 1 else str(date[1])
                    year = str(date[2])
                    date_in_format = year + "-" + month + "-" + day
                    window2["_ending_"](date_in_format)

                if event == "_savebutton_":
                    if (values["_subscription_"] == "") or \
                    (values["_price_"] == "") or \
                    (values["_ending_"] == ""):
                        psg.Popup("Ошибка", "Заполните все поля формы.")
                        continue
                    new_service_name = values["_subscription_"]
                    new_state_id = db_driver.get_id_by_state(values["_state_"])
                    new_duration_id = db_driver.get_id_by_duration(values["_duration_"])
                    new_price = values["_price_"]
                    new_term_end = values["_ending_"]
                    tuple_to_save = (id_to_update, new_service_name, new_state_id, new_duration_id, new_price, new_term_end)
                    db_driver.update_sub(tuple_to_save)
                    psg.Popup("Редактирование", "Подписка изменена!")
                    window["_table_"](util.TableMaker.make_basic_table(db_driver))
            window2.close()

        if event == "_deletebutton_":
            if len(values["_table_"]) == 0:
                psg.Popup("Ошибка", "Не выбрана запись для удаления")
                continue
            row_number = values["_table_"][0]
            table_data = util.TableMaker.make_basic_table(db_driver)
            service_name_to_delete = table_data[row_number][0]
            id_to_delete = db_driver.get_sub_id_by_name(service_name_to_delete)
            db_driver.delete_sub(id_to_delete)
            psg.Popup("Удаление", "Выбранная подписка успешно удалена!")
            window["_table_"](util.TableMaker.make_basic_table(db_driver))
        if event == "_checkbutton_":
            if notifier.check_updates(db_driver)>0:
                window["_table_"](util.TableMaker.make_basic_table(db_driver))
            else:
                psg.Popup("Все обновлено", "В системе нет подписок, актуальных для продления.")
    window.close()


if __name__=="__main__":
    main()