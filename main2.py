import sqlite3


def count_premia(time_worked_on_week):
    if time_worked_on_week > 40:
        return 800 * (time_worked_on_week - 40)

    if time_worked_on_week < 25:
        return 'уволен'
def count_formula(id):
    cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo = list(
        cur.execute(f"SELECT * from worktime where id={id}").fetchall()[0][1:])
    exit_time = time_to_float(input("введите время ухода"))
    time_worked_on_week += exit_time - cum_time
    worked_days += 1
    if worked_days == 5:
        print("канец нидили")
        prem = count_premia(time_worked_on_week)
        if prem == "уволен":
            print("сотрудник увольняется! увольте вручную")
        else:
            premia_nakapalo += prem
            time_worked_on_week = 0

            worked_weeks += 1
            if worked_weeks == 4:
                print("выдайте премию и зарплату!")
                worked_weeks = 0
        worked_days = 0
    return ", ".join(list(map(str, [cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo])))

def time_to_float(time):
    time = time.split(":")
    return int(time[0]) + int(time[1]) / 60



con = sqlite3.connect("maindb.db")
cur = con.cursor()
for i in cur.execute("SELECT id, name, surname, salary from main_sotrud"):
    for j in i:
        print(j, end=" ")
    print()
while True:
    deyst = int(input("1 - сотрудник пришел, 2 - сотрудник ушел"))
    if deyst == 1:
        id = input("введите id сотрудника")
        try:
            needed_values = ", ".join(list(map(str, list(cur.execute(f"SELECT time_worked_on_week, worked_days, worked_weeks, premia_nakapalo from worktime where id={id}").fetchall()[0]))))
        except IndexError:
            needed_values = "0, 0, 0, 0"
        cur.execute(f"INSERT OR REPLACE into worktime (id, cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo) VALUES ({id}, {str(time_to_float(input('введите время')))}, {needed_values})")
        con.commit()
    if deyst == 2:
        id = input("введите id")
        cur.execute(f"INSERT OR REPLACE into worktime (id, cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo) VALUES ({id}, {count_formula(id)})")
        con.commit()