from datetime import datetime, timedelta
import mysql.connector
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