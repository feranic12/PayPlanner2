import PySimpleGUI as psg
import db
import util
import datetime
import os.path
from MatPlotLibHelper import MatPlotLibHelper

def main():
    db_driver = db.DB(os.path.abspath("pay_planner2_db.db"))
    notifier = util.Notifier(db_driver)
    notifier.check_updates(db_driver)

    # главное окно приложения - window
    table_data = util.TableMaker.make_basic_table(db_driver)
    header_list = ["Название сервиса", "Состояние подписки",
                   "Период продления","Сумма", "Срок окончания"]
    my_table = psg.Table(values = table_data,
                headings=header_list,
               justification="left", bind_return_key=True, key="_table_")
    layout = [[my_table],
        [psg.Button("Добавить", key="_addbutton_"), psg.Button("Редактировать", key="_editbutton_"),
         psg.Button("Удалить", key="_deletebutton_"), psg.Button("Проверить", key="_checkbutton_"),
         psg.Button("Сумма за период", key="_sumbutton_"), psg.Button("Диаграмма", key="_diagrambutton_")]
    ]
    window = psg.Window('Главное окно', layout, icon="icons/icon1.ico")

    while True:
        event, values = window.read(timeout=100)
        if event in (None, "Exit", "Cancel"):
            break
        if event == "_addbutton_":
            # окно добавления подписки window1
            layout1_maker = util.Layout1Maker(db_driver)
            layout1 = layout1_maker.make_layout1()
            window1 = psg.Window("Добавление подписки", layout1, modal=True, icon="icons/icon1.ico")
            while True:
                event, values = window1.read(timeout=100)
                if event in (None, "Exit"):
                    break
                if event == "_termend_":
                    input_date = psg.popup_get_date()
                    if input_date is None:
                        continue
                    date_in_format = util.get_date_in_format(input_date)
                    window1["_ending_"](date_in_format)
                if event == "_savebutton_":
                    if (values["_subscription_"] == "") or \
                    (values["_price_"] == "") or \
                    (values["_ending_"] == ""):
                        psg.Popup("Ошибка", "Заполните все поля формы.", icon="icons/icon1.ico")
                        continue
                    service_name = values["_subscription_"]
                    state_id = db_driver.get_id_by_state(values["_state_"])
                    duration_id = db_driver.get_id_by_duration(values["_duration_"])
                    price = values["_price_"]
                    term_end = values["_ending_"]
                    tuple_to_add = (service_name, state_id, duration_id, price, term_end)
                    db_driver.add_subscription_to_db(tuple_to_add)
                    psg.Popup("Добавление", "Новая подписка успешно добавлена!", icon="icons/icon1.ico")
                    window["_table_"](util.TableMaker.make_basic_table(db_driver))
            window1.close()
            
        if event == "_editbutton_" or event == "_table_":
            if len(values["_table_"]) == 0:
                psg.Popup("Ошибка", "Не выбрана запись для редактирования", icon="icons/icon1.ico")
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

            # окно редактирования подписки window2

            layout2_maker = util.Layout2Maker(db_driver, tuple_to_update)
            layout2 = layout2_maker.make_layout2()
            window2 = psg.Window("Редактирование подписки", layout2, modal=True, icon="icons/icon1.ico")
            while True:
                event, values = window2.read()
                if event in (None, "Exit", "Cancel"):
                    break
                if event == "_termend_":
                    input_date = psg.popup_get_date()
                    if input_date is None:
                        continue
                    date_in_format = util.get_date_in_format(input_date)
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
                    psg.Popup("Редактирование", "Подписка изменена!", icon="icons/icon1.ico")
                    window["_table_"](util.TableMaker.make_basic_table(db_driver))
            window2.close()

        # удаление выбранной подписки
        if event == "_deletebutton_":
            if len(values["_table_"]) == 0:
                psg.Popup("Ошибка", "Не выбрана запись для удаления", icon="icons/icon1.ico")
                continue
            row_number = values["_table_"][0]
            table_data = util.TableMaker.make_basic_table(db_driver)
            service_name_to_delete = table_data[row_number][0]
            id_to_delete = db_driver.get_sub_id_by_name(service_name_to_delete)
            db_driver.delete_sub(id_to_delete)
            psg.Popup("Удаление", "Выбранная подписка успешно удалена!")
            window["_table_"](util.TableMaker.make_basic_table(db_driver))

        # проверка наличия пригодных для продления подписок, и, если они есть, отправка уведомления в Windows
        if event == "_checkbutton_":
            if notifier.check_updates(db_driver)>0:
                window["_table_"](util.TableMaker.make_basic_table(db_driver))
            else:
                psg.Popup("Все обновлено", "В системе нет подписок, актуальных для продления.", icon="icons/icon1.ico")

        # вызов формы суммирования подписок
        if event == "_sumbutton_":
            today = datetime.datetime.today()
            today_str = datetime.datetime.strftime(today, "%Y-%m-%d")
            layout3 = [
                [psg.Text("Начало срока"), psg.Input(key="_sumstartinput_", disabled=True, default_text=today_str),
                    psg.Button("Выбрать дату", key="_sumstartbutton_")],
                [psg.Text("Конец срока"), psg.Input(key="_sumendinput_", disabled=True, default_text=today_str),
                    psg.Button("Выбрать дату", key="_sumendbutton_")],
                 [psg.Button("Посчитать", key="_countbutton_")]
            ]
            window3 = psg.Window("Сумма за период", layout3, modal=True, icon="icons/icon1.ico")
            date1 = date2 = today.date()
            while True:
                event, values = window3.Read()
                if event in (None, "Exit"):
                    break
                if event == "_sumstartbutton_":
                    input_date = psg.popup_get_date()
                    if input_date is None:
                        continue
                    date1 = datetime.datetime.strptime(util.get_date_in_format(input_date), "%Y-%m-%d").date()
                    window3['_sumstartinput_'](date1)
                if event == "_sumendbutton_":
                    input_date = psg.popup_get_date()
                    if input_date is None:
                        continue
                    date2 = datetime.datetime.strptime(util.get_date_in_format(input_date), "%Y-%m-%d").date()
                    window3['_sumendinput_'](date2)
                # подсчет суммарной стоимости подписок за период
                if event == "_countbutton_":
                    subs = db_driver.get_all_subscriptions()
                    if date1 > date2:
                        psg.Popup("Ошибка!", "Дата начала периода превосходит дату его окончания!", icon="icons/icon1.ico")
                        break
                    sum_price = util.calculate_sum_price(db_driver, subs, date1, date2)
                    if sum_price is None:
                        sum_price = 0
                    psg.Popup("Сумма", "Сумма расходов за выбранный период: {0} рублей ".format(sum_price), icon="icons/icon1.ico")
            window3.close()
        if event == "_diagrambutton_":
            layout4 = [[psg.Canvas(key="_canvas_")]]
            window4 = psg.Window("Диаграмма", layout4, finalize=True)
            fig = MatPlotLibHelper.draw_figure_mpl()
            MatPlotLibHelper.draw_figure_psg(window4["_canvas_"].TKCanvas, fig)
            event, values = window4.read()
            window4.close()




if __name__=="__main__":
    main()