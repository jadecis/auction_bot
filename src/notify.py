from loader import db, bot 
from datetime import datetime
import aioschedule, asyncio

async def check_result():
    result= db.get_games(result=True)
    if result:
        for i in result:
            # left=  i[5]-datetime.timestamp(datetime.now())
            if datetime.timestamp(datetime.now()) >= i[5]:
                if db.count_users(i[2]) == 1:
                    db.up_balance(user_id=i[1], sum=i[3]*1.1)
                    user= db.get_user(i[1])
                    name= f"@{user[2]}" if user[2] else f"<b>{user[4]}</b>"
                    await bot.send_message(chat_id=i[1], text=f"👨🏻‍⚖️ Аукцион <code>#{i[2]}</code>\n"
                                            +f"<b>{name} ВЫИГРЫВАЕТ round({i[3] *1.1}, 1) рублей!</b>"
                                            )
                    db.delete_auction(i[2])
                else: 
                    user=db.last_bet(i[2])
                    db.up_balance(user_id=user[1], sum=i[3]*0.9)
                    db.add_desc(i[2], type='win')    
            # elif (left <= 610) and left >= 540:
            #     db.add_desc(i[2], type='last')
    
    
async def rassilka():
    result= db.get_desc()
    if result:
        for i in result:
            if i[2] == 'win':
                history= db.get_allbets(i[1])
                last_bet= db.last_bet(i[1])
                user= db.get_user(last_bet[1])
                info= db.get_game_Byid(i[1])
                for j in history:
                    try:
                        name= f"@{user[2]}" if user[2] else f"<b>{user[4]}</b>"
                        await bot.send_message(chat_id=j[1], text=f"👨🏻‍⚖️ Аукцион <code>#{i[1]}</code>\n"
                                            +f"<b>{name} ВЫИГРЫВАЕТ {round(info[3] *0.9, 1)} рублей!</b>"
                                            )
                    except Exception as ex:
                        print(ex)
                db.delete_auction(i[1])
                
            # elif i[2] == 'last':
            #     history= db.get_allbets(i[1])
            #     for j in history:
            #         try:
            #             await bot.send_message(chat_id=j[1], text=f"👨🏻‍⚖️ Аукцион <code>#{i[1]}</code>\n"
            #                                 +f"<b>Закачивается через 10 минут!</b>"
            #                                 )
            #         except Exception as ex:
            #             print(ex)
            else:
                last_bet= db.last_bet(i[1])
                history= db.get_allbets(i[1], last_bet[1])
                info= db.get_game_Byid(i[1])
                for j in history:
                    try:
                        user= db.get_user(last_bet[1])
                        name= f"@{user[2]}" if user[2] else f"<b>{user[4]}</b>"
                        await bot.send_message(chat_id=j[1], text=f"👨🏻‍⚖️ Аукцион <code>#{i[1]}</code>\n\n"
                                            +f"{name} повысил ставку до <b>{info[3]} рублей!</b>\n"
                                            "Успевай перебить ставку, у тебя есть 15 минут"
                                            )
                    except Exception as ex:
                        print(ex)
            db.del_desc(i[0])
                    
async def scheduler():
    aioschedule.every().minute.do(check_result)
    aioschedule.every().second.do(rassilka)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)