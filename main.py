import PySimpleGUI as psg
import db
from util import Util


def main():
    db_driver = db.DB("pay_planner2_db.db")
    layout1 = Util.layout1_setup(db_driver)
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
        if event == "_addbutton_":
            layout1 = Util.layout1_setup(db_driver)
            window1 = psg.Window("Добавление подписки", layout1)
            while True:
                event, values = window1.read(timeout=100)
                if event in (None, 'Exit'):
                    break
                if event == "_termend_":
                    date = psg.popup_get_date()
                    month = "0" + str(date[0]) if len(str(date[0])) == 1 else str(date[0])
                    day = "0" + str(date[1]) if len(str(date[1])) == 1 else str(date[1])
                    year = str(date[2])
                    date_in_format = year + "-" + month + "-" + day
                    window1["_ending_"](date_in_format)
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
            window1.close()
            
        if event == "_editbutton_" or event == "_table_":
            if len(values["_table_"]) == 0:
                psg.Popup("Ошибка", "Не выбрана запись для редактирования")
                continue
            layout2 = layout1
            window2 = psg.Window("Редактирование записи", layout2)
                
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