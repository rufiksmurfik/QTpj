import sqlite3
cur = sqlite3.connect("maindb.db").cursor()
id = 1

cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo = list(cur.execute(f"SELECT * from worktime where id={id}").fetchall()[0][1:])
print(cum_time)