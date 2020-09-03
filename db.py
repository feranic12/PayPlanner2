import sqlite3


# класс, реализующий взаимодействие с базой данных
class DB:
    def __init__(self, filepath):
        self.con = sqlite3.connect(filepath)

    # подсчет числа записей в таблице "подписки"
    def get_subs_count(self):
        cur = self.con.cursor()
        cur.execute("select count(*) from subscriptions")
        result = cur.fetchone()[0]
        cur.close()
        return result

    # получение списка всех подписок
    def get_all_subscriptions(self):
        cur = self.con.cursor()
        cur.execute("select * from subscriptions")
        result = cur.fetchall()
        cur.close()
        return result

    # получение выборки из нескольких таблиц БД, для заполнения таблицы в главном окне
    def get_subs_for_table(self):
        cur = self.con.cursor()
        cur.execute("""select s.service_name, st.name, d.duration, s.price, s.term_end 
                    from subscriptions s join states st on s.state_id = st.id 
                    join durations d on s.duration_id = d.id""")
        result = cur.fetchall()
        return result

    # получение всех состояний для ComboBox
    def get_all_states(self):
        cur = self.con.cursor()
        sql = """select name from states"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result

    # получение всех длительностей для Combobox
    def get_all_durations(self):
        cur = self.con.cursor()
        sql = """select duration + " мес." from durations"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result

    # получение длительности по id
    def get_id_from_duration(self, duration):
        cur = self.con.cursor()
        cur.execute("select id from durations where duration = ?", [duration])
        result = cur.fetchone()[0]
        cur.close()
        return result

    def get_id_from_state(self, state):
        cur = self.con.cursor()
        cur.execute("select id from states where state = ?", [state])
        result = cur.fetchone()[0]
        cur.close()
        return result

    # добавление новой подписки в БД
    def add_subscription_to_db(self, t):
        cur = self.con.cursor()
        cur.execute("select max(id) from subscriptions")
        n = cur.fetchone()[0]
        try:
            cur.execute("insert into subscriptions values(?,?,?,?,?,?,?)", n+1, t[0], t[1], t[2], t[3], t[4], t[5])
        except sqlite3.DatabaseError as err:
            print("Ошибка работы с БД " + err)
        self.con.commit()
        cur.close()

    # получение текущей подписки
    def get_current_sub(self, id):
        cur = self.con.cursor()
        cur.execute("select * from subscriptions where id = ?", [id])
        result = cur.fetchone()
        cur.close()
        return result

    # обновление текущей подписки
    def update_sub(self, t):
        cur = self.con.cursor()
        sql = """update subscriptions set service_name = ?, state_id = ?,
                  duration_id = ?, price = ?, term_end = ? where id = ?"""
        cur.execute(sql,[t[1], t[2], t[3], t[4], t[5], t[0]])
        self.con.commit()
        cur.close()

    # удаление текущей подписки
    def delete_sub(self, id):
        cur = self.con.cursor()
        try:
            cur.execute("delete from subscriptions where id=?",[id])
        except sqlite3.DatabaseError as err:
            print(err)
        self.con.commit()
        cur.close()

    # обновление конечной даты подписки при ее продлении
    def update_end_date(self, id, date):
        cur = self.con.cursor()
        cur.execute("update subscriptions set term_end = ? where id = ?", [date, id])
        self.con.commit()
        cur.close()

    def __del__(self):
        self.con.close()