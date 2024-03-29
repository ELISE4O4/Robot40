#!/usr/bin/env python3

#
# اپن شد برای اولین بار در کانال آیرا تیم منبع نزنی بی ناموسی

# @IRA_Team
# https://t.me/IRA_Team
#

import os
import sys
import time
import pymysql.cursors
from telethon.sync import TelegramClient
from telethon import errors
import utility as utl

for index, arg in enumerate(sys.argv):
    if index == 1:
        from_id = arg
if len(sys.argv) != 2:
    print("Invalid parameters!")
    exit()

directory = os.path.dirname(os.path.abspath(__file__))
timestamp = int(time.time())
cs = pymysql.connect(host=utl.host_db, user=utl.user_db, password=utl.passwd_db, database=utl.database, port=utl.port, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
cs = cs.cursor()

cs.execute(f"SELECT * FROM {utl.admini}")
row_admin = cs.fetchone()

list_files = os.listdir(f"{directory}/import")
count_all = len(list_files)
count_import = count_failed_import = 0
info_msg = utl.bot.send_message(
    chat_id=from_id,
    text="Ongoing operation ..."
)
for file in list_files:
    timestamp = int(time.time())
    row_apis = utl.select_api(cs,row_admin['api_per_number'])
    if row_apis is None:
        utl.bot.send_message(chat_id=from_id,text="❌ No Api found")
        break
    else:
        try:
            client = TelegramClient(session=f"{directory}/import/{file}",api_id=row_apis['api_id'],api_hash=row_apis['api_hash'])
            client.connect()
            if client.is_user_authorized():
                me = client.get_me()
                phone = me.phone
                cs.execute(f"SELECT * FROM {utl.mbots} WHERE phone='{phone}'")
                row_mbots = cs.fetchone()
                if row_mbots is None:
                    client.disconnect()
                    os.rename(f"{directory}/import/{file}", f"{directory}/sessions/{phone}.session")
                    uniq_id = utl.uniq_id_generate(cs,10,utl.mbots)
                    cs.execute(f"INSERT INTO {utl.mbots} (creator_user_id,phone,user_id,status,api_id,api_hash,created_at,uniq_id) VALUES ('{from_id}','{phone}','{me.id}','submitted','{row_apis['api_id']}','{row_apis['api_hash']}','{timestamp}','{uniq_id}')")
                    count_import += 1

            else:
                count_failed_import += 1
                print(f"not auth: {file}")
            try:
                info_msg.edit_text(
                    text="Ongoing operation ...\n\n"
                        f"checking => [{(count_import + count_failed_import):,} / {count_all:,}]\n" +
                        f"success => {count_import:,}",
                )
            except:
                pass
        except Exception as e:
            error = str(e)
            print(f"Error2: {error}")
            if "database is locked" in error:
                utl.bot.send_message(chat_id=from_id,text="❌ Kill the processes and run the robot again")
            elif "You have tried logging in too many times" in error:
                utl.bot.send_message(chat_id=from_id,text="❌ This phone number is limited due to a lot of effort, try again 24 hours later")
            else:
                utl.bot.send_message(chat_id=from_id,text=f"❌ Unknown error\n\n{error}")
        finally:
            try:
                client.disconnect()
            except:
                pass
utl.bot.send_message(chat_id=from_id,text=f"{count_import} accounts were added")


#
# اپن شد برای اولین بار در کانال آیرا تیم منبع نزنی بی ناموسی

# @IRA_Team
# https://t.me/IRA_Team
#