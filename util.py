import PySimpleGUI as psg
import time
from datetime import date, timedelta, datetime
from plyer import notification


# класс, формирующий таблицу в главном окне
class TableMaker:
    def make_basic_table(db_driver):
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
        return table_data


# базовый класс, реализующий общую часть формирования разметки форм добавления и радектирования подписки
class BaseLayoutMaker:
    def __init__(self):
        self.states_list = []
        self.duration_list = []
        self.durations_by_db = self.db_driver.get_all_durations()
        self.states_by_db = self.db_driver.get_all_states()
        for st in range(0, len(self.states_by_db)):
            self.states_list.append(str(self.states_by_db[st][0]))
        for dur in range(0, len(self.durations_by_db)):
            self.duration_list.append(str(self.durations_by_db[dur][0]))


# класс, генерирующий разметку формы добавления подписки
class Layout1Maker(BaseLayoutMaker):
    def __init__(self, db_driver):
        self.db_driver = db_driver
        BaseLayoutMaker.__init__(self)

    def make_layout1(self):
        return [[psg.Text("Название подписки:"), psg.Input(key="_subscription_")],
                [psg.Text("Статус:"), psg.Combo(self.states_list, default_value=self.states_list[0], key="_state_"),
                 psg.Text("Срок продления:"),
                 psg.Combo(self.duration_list, default_value=self.duration_list[0], key="_duration_"),
                 psg.Text("мес.")],
                [psg.Text("Сумма списания:"), psg.Input(key="_price_")],
                [psg.Text("Срок окончания:"), psg.Input(disabled=True, key="_ending_"),
                 # psg.CalendarButton("Выбрать дату", target="_ending_", key="_termend_", format="%Y-%m-%d")],
                 psg.Button("Выбрать дату", key="_termend_")],
                [psg.Button("Сохранить", key="_savebutton_")]]


# класс, генерирующий разметку формы редактирования подписки
class Layout2Maker(BaseLayoutMaker):
    def __init__(self, db_driver, t):
        self.db_driver = db_driver
        BaseLayoutMaker.__init__(self)
        self.service_name_default = t[1]
        self.state_default = db_driver.get_state_by_id(t[2])
        self.duration_default = db_driver.get_duration_by_id(t[3])
        self.price_default = t[4]
        self.termend_default = t[5]

    def make_layout2(self):
        db_driver = self.db_driver
        return [[psg.Text("Название подписки:"), psg.Input(key="_subscription_", default_text=self.service_name_default)],
                [psg.Text("Статус:"), psg.Combo(self.states_list, default_value=self.state_default, key="_state_"),
                 psg.Text("Срок продления:"),
                 psg.Combo(self.duration_list, default_value=self.duration_default, key="_duration_"),
                 psg.Text("мес.")],
                [psg.Text("Сумма списания:"), psg.Input(key="_price_", default_text=self.price_default) ],
                [psg.Text("Срок окончания:"), psg.Input(disabled=True, key="_ending_", default_text=self.termend_default),
                 # psg.CalendarButton("Выбрать дату", target="_ending_", key="_termend_", format="%Y-%m-%d")],
                 psg.Button("Выбрать дату", key="_termend_")],
                [psg.Button("Сохранить", key="_savebutton_")]]


# класс, анализирующий подписки и выдающий объявления
class Notifier:
    def __init__(self, db_driver):
        self.db_driver = db_driver

    # анализ подписок, подсчет числа подписок, подлежащих продлению
    def check_updates(self, db_driver):
        subs = self.db_driver.get_all_subscriptions()
        # n - число подписок, оканчивающихся сегодня или завтра
        n = 0
        for sub in subs:
            # если подписка не прервана
            if sub[2] != 2:
                end_date = datetime.strptime(sub[5], "%Y-%m-%d").date()
                if end_date <= date.today() + timedelta(1):
                    n = n + 1
                    time.sleep(5)
                    self.send_notification(sub)
                # увеличение даты окончания периода подписки на месяц/год
                while end_date <= date.today():

                    # ежемесячная подписка
                    duration = self.db_driver.get_duration_by_id(sub[3])
                    if end_date.month + duration <= 12:
                        end_date = date(end_date.year, end_date.month + duration, end_date.day)
                    else:
                        end_date = date(end_date.year + 1, end_date.month + duration - 12, end_date.day)
                    self.db_driver.update_end_date(sub[0], end_date)
        return n

    # отправка оповещения в трей Windows
    def send_notification(self, sub):
        # если подписка не прервана
        if sub[2] != 2:
            notification.notify(
                title='ПОДПИСЧИК',
                message=sub[5] + ' истекает срок продления подписки ' + sub[1] + ' . Будет списано ' + str(sub[4]) + ' рублей',
                app_name='PayPlanner',
                app_icon='icons/icon1.ico'
            )


# преобразование даты, полученной с помощью popup_get_date, к требуемому формату.
def get_date_in_format(input_date):
    month = "0" + str(input_date[0]) if len(str(input_date[0])) == 1 else str(input_date[0])
    day = "0" + str(input_date[1]) if len(str(input_date[1])) == 1 else str(input_date[1])
    year = str(input_date[2])
    date_in_format = year + "-" + month + "-" + day
    return date_in_format


# подсчет суммарной стоимсти подписок за период
def calculate_sum_price(db_driver, start_date, end_date):
    result_sum = 0
    subs = db_driver.get_all_subscriptions()
    for sub in subs:
        next_date = datetime.strptime(sub[5], "%Y-%m-%d").date()
        duration = db_driver.get_duration_by_id(sub[3])
        if next_date >= start_date:
            while next_date <= end_date:
                result_sum += sub[4]
                if next_date.month + duration <= 12:
                    next_date = date(next_date.year, next_date.month + duration, next_date.day)
                else:
                    next_date = date(next_date.year + 1, next_date.month + duration - 12, next_date.day)
    return result_sum

# def calculate_sum_price_for_month(db_driver, subs, month)
