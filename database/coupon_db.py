import sqlite3 as sq

def sq_start():
    global db, cur
    db = sq.connect("couponbot_db.db")
    cur = db.cursor()

    if db:
        print('Database connected successfully')
    db.execute("""create table if not exists users(
    tg_id int,
    name text,
    number int)
    """)
    db.execute("""create table if not exists coupons(
    shop text,
    description text,
    coupon text)
    """)
    db.commit()


def registration(tg_id,name, number):
    cur.execute("insert into users values(?,?,?);",(tg_id,name,number))
    db.commit()

def check_registration(number):
    cur.execute(f"select * from users where number='{number}'")
    return cur.fetchall()

def get_promo():
    cur.execute(f"select coupon from coupons")
    return  cur.fetchall()

def get_description(coupon):
    cur.execute(f"select * from coupons where coupon='{coupon}'")
    return cur.fetchall()