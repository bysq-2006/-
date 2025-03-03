from flask import Flask, request, redirect, url_for, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector
import atexit
from datetime import datetime, timedelta
from config import db_config, switch_Remaining_time_reduce_one, Remaining_time_

def Remaining_time_reduce_one():
    if switch_Remaining_time_reduce_one:
        try:
            # 连接到数据库
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # 更新Remaining_time字段
            cursor.execute("UPDATE time SET Remaining_time = Remaining_time - 1 WHERE id = 1")
            conn.commit()

            # 检查更新结果
            cursor.execute("SELECT Remaining_time FROM time WHERE id = 1")
            result = cursor.fetchone()
            if result:
                print(f"定时任务正在执行... Remaining_time: {result[0]}")
            else:
                print("记录未找到")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

def my_scheduled_job():
    global Remaining_time_
    try:
        # 连接到数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 获取当前时间和七天后的时间
        start_time = datetime.now()
        end_time = start_time + timedelta(days=7)

        # 获取Remaining_time的值
        cursor.execute("SELECT Remaining_time FROM time WHERE id = 1")
        result = cursor.fetchone()
        if result:
            length = result[0]

            # 在Records表中插入一条新记录
            cursor.execute(
                "INSERT INTO Records (start_time, end_time, length) VALUES (%s, %s, %s)",
                (start_time, end_time, Remaining_time_ - length)
            )
            conn.commit()
            print(f"定时任务执行成功... ")
        else:
            print("记录未找到")

        # 更新Remaining_time字段
        cursor.execute("UPDATE time SET Remaining_time = %s WHERE id = 1", (Remaining_time_,))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

app = Flask(__name__)

# 创建调度器，定时任务执行间隔为1秒
scheduler = BackgroundScheduler()
scheduler.add_job(func=Remaining_time_reduce_one, trigger="interval", seconds=1)
# 每周一零点触发的任务
scheduler.add_job(my_scheduled_job, 'cron', day_of_week='mon', hour=0, minute=0)
scheduler.start()

# 确保在程序退出时调度器也停止
atexit.register(lambda: scheduler.shutdown())

@app.route('/set_switch', methods=['POST'])
def set_switch():
    global switch_Remaining_time_reduce_one
    switch_Remaining_time_reduce_one = not switch_Remaining_time_reduce_one
    return redirect(url_for('index'))

@app.route('/')
def index():
    try:
        # 连接到数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 获取Remaining_time的值
        cursor.execute("SELECT Remaining_time FROM time WHERE id = 1")
        result = cursor.fetchone()
        if result:
            current_time = result[0]
        else:
            current_time = Remaining_time_

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        current_time = Remaining_time_
    finally:
        cursor.close()
        conn.close()

    return render_template('main.html', total_time=Remaining_time_, current_time=current_time, switch=switch_Remaining_time_reduce_one)

@app.route('/list')
def list_records():
    try:
        # 连接到数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 获取所有记录
        cursor.execute("SELECT id, start_time, end_time, length FROM Records ORDER BY id DESC")
        records = cursor.fetchall()

        # 计算总学习时间和平均学习时间
        cursor.execute("SELECT SUM(length), AVG(length) FROM Records")
        total_time, average_time = cursor.fetchone()

        # 计算总天数
        cursor.execute("SELECT MIN(start_time), MAX(end_time) FROM Records")
        start_time, end_time = cursor.fetchone()
        total_days = (end_time - start_time).days if start_time and end_time else 0

        # 检查 total_time 和 average_time 是否为 None
        if total_time is None:
            total_time = 0
        if average_time is None:
            average_time = 0

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        records = []
        total_time = 0
        average_time = 0
        total_days = 0
    finally:
        cursor.close()
        conn.close()

    return render_template('list.html', records=records, total_time=total_time / 3600, average_time=average_time / 3600, total_days=total_days)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')  # 如果设置为True，调度器会每秒执行两次
