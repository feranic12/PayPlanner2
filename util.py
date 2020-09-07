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
