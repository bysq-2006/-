## 这是一个自主督促学习的网站
### 功能有：
1. 拥有一个倒计时，点击单开关切换，可设置时间，每星期重置一次。
2. 一个表单，可以统计从启动这个程序到目前为止的所有学习情况。


~~知识太过于薄弱，基于gpt-o4的编程，在写到前端那个界面的时候大概就发现自己写的是一坨屎山了,
不过倒也能用~~<br>
**需要提前安装mysql数据库**<br><br>
然后连接数据库输入以下语句:
```
-- 创建数据库 learning
CREATE DATABASE learning;

-- 使用数据库 learning
USE learning;

-- 创建表 time
CREATE TABLE time (
    id INT PRIMARY KEY,
    Remaining_time INT
);

-- 创建表 Records
CREATE TABLE Records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    start_time DATE,
    end_time DATE,
    length INT
);

-- 插入数据到表 time
INSERT INTO time (id, Remaining_time) VALUES (1, 3600);
```
*注:Remaining_time 单位为秒*

**你需要在Python环境下输入以下语句，来安装第三方库**
```
pip install Flask APScheduler mysql-connector-python
```

**请注意在config.py 内部配置你的数据库信息**
```
# 数据库配置
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'learning'
}
```
**以及每周学习的时间**
```
Remaining_time_:int = 18000 # 剩余时间, 单位: 秒
```

然后，在终端输入python app.py