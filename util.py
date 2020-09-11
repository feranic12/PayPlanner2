import PySimpleGUI as psg


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


class BaseLayoutMaker:
    def __init__(self, db_driver):
        self.states_list = []
        self.duration_list = []
        self.durations_from_db = db_driver.get_all_durations()
        self.states_from_db = db_driver.get_all_states()
        for st in range(0, len(self.states_from_db)):
            self.states_list.append(str(self.states_from_db[st][0]))
        for dur in range(0, len(self.durations_from_db)):
            self.duration_list.append(str(self.durations_from_db[dur][0]))


class Layout1(BaseLayoutMaker):
    def __init__(self, db_driver):
        BaseLayoutMaker.__init__(self, db_driver)

    def make_layout1(self, db_driver):
        return [[psg.Text("Название подписки:"), psg.Input(key="_subscription_")],
                [psg.Text("Статус:"), psg.Combo(self.states_list, default_value=self.states_list[0], key="_state_"),
                 psg.Text("Срок продления:"),
                 psg.Combo(self.duration_list, default_value=self.duration_list[0], key="_duration_"),
                 psg.Text("мес.")],
                [psg.Text("Сумма списания:"), psg.Input(key="_price_")],
                [psg.Text("Срок окончания:"), psg.Input(disabled=True, key="_ending_"),
                 # psg.CalendarButton("Выбрать дату", target="_ending_", key="_termend_", format="%Y-%m-%d")],
                 psg.Button("Выбрать дату", key="_termend_")],
                [psg.Button("Сохранить")]]


class Layout2(BaseLayoutMaker):
    def __init__(self, db_driver):
        BaseLayoutMaker.__init__(self, db_driver)



    def make_layout2(self, db_driver):
        return [[psg.Text("Название подписки:"), psg.Input(key="_subscription_")],
                [psg.Text("Статус:"), psg.Combo(self.states_list, default_value=self.states_list[0], key="_state_"),
                 psg.Text("Срок продления:"),
                 psg.Combo(self.duration_list, default_value=self.duration_list[0], key="_duration_"),
                 psg.Text("мес.")],
                [psg.Text("Сумма списания:"), psg.Input(key="_price_")],
                [psg.Text("Срок окончания:"), psg.Input(disabled=True, key="_ending_"),
                 # psg.CalendarButton("Выбрать дату", target="_ending_", key="_termend_", format="%Y-%m-%d")],
                 psg.Button("Выбрать дату", key="_termend_")],
                [psg.Button("Сохранить")]]
