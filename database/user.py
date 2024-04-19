from typing import Optional
from sqlalchemy import select, insert
from .model import User
from .setup  import async_session  
import datetime



async def select_user(user_id: int) -> Optional[User]:
    async with async_session() as session:
        select_stmt = select(User).where((User.user_id == user_id) & (User.banned ==False))

        result = await session.execute(select_stmt)
        return result.scalar_one_or_none()
    

async def check(user_id: int) -> Optional[User]:
    async with async_session() as session:
        select_stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(select_stmt)
        return result.scalar_one_or_none()


async def add_user(user_id: int , gender:str) -> None:
    async with async_session() as session:
        insert_stmt = insert(User).values(user_id=user_id ,gender= gender)
        await session.execute(insert_stmt)
        await session.commit()




async def delete_user(user_id: int) -> None:
    async with async_session() as session:
        stmt = delete(User).where(User.user_id == user_id)
        await session.execute(stmt)
        await session.commit()        
        await session.close()



async def is_user_banned(user_id: int) -> bool:
    async with async_session() as session:
        select_stmt = select(User.banned).where(User.user_id == user_id)
        result = await session.execute(select_stmt)
        return result.scalar()  # Assumes the 'banned' colum
    



async def update_bonus_count(user_id: int):
    async with async_session() as session:
        try:
            stmt = (update(User).where(User.user_id == user_id).values(bonus_count=User.bonus_count + 1))
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            print(f"Error updating bonus count: {str(e)}")


async def is_user_present(user_id: int) -> bool:
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        return bool(result.scalar_one_or_none())


from sqlalchemy import asc, delete, desc, func, insert, not_, or_, select, update
from typing import Optional
from database.model import Queue, User



async def in_search(user_id: int) -> bool:
    async with async_session() as session:
        stmt = select(Queue).where(Queue.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None



async def enlist_user( user_id: int) -> None:
    async with async_session() as session:
        stmt = insert(Queue).values(user_id=user_id)
        await session.execute(stmt)
        await session.commit()
        await session.close()



async def delist_user(user_id: int) -> None:
    async with async_session() as session:
        stmt = delete(Queue).where(Queue.user_id == user_id)
        await session.execute(stmt)
        await session.commit()        
        await session.close()






async def delete_match(user_id,partner_id):
    async with async_session() as session:
        # Use the update statement to set the partner_id for the given user_id
        update_stmt1 = (update(User).where(User.user_id == user_id).values(partner_id=None , previous_id=partner_id , chat_count=User.chat_count + 1))
        update_stmt2 = (update(User).where(User.user_id == partner_id).values(partner_id=None, previous_id=user_id, chat_count=User.chat_count + 1))
        await session.execute(update_stmt1)
        await session.execute(update_stmt2)
        await session.commit()
        await session.close()




async def make_user_premium(user_id: int, days: int):
    async with async_session() as session:
        # Calculate the VIP expiry date (based on the provided number of days)
        vip_expiry_date = datetime.datetime.now() + datetime.timedelta(days=days)
        # Update the User record in the database
        stmt = (update(User).where(User.user_id == user_id).values(premium=True, vip_expiry=vip_expiry_date))
        await session.execute(stmt)
        await session.commit()
        await session.close()


   
async def update_user_ugender(user_id: int, gender: str):
    async with async_session() as session:
        stmt = update(User).where(User.user_id == user_id).values(gender=gender)
        await session.execute(stmt)
        await session.commit()


async def delete_user_gender(user_id: int):
    async with async_session() as session:
        stmt = update(User).where(User.user_id == user_id).values(gender=None)
        await session.execute(stmt)
        await session.commit()


async def update_user_pgender(user_id: int, pgender: str):
    async with async_session() as session:
        stmt = update(User).where(User.user_id == user_id).values(pgender=pgender)
        await session.execute(stmt)
        await session.commit()


async def delete_user_pgender(user_id: int):
    async with async_session() as session:
        stmt = update(User).where(User.user_id == user_id).values(pgender=None)
        await session.execute(stmt)
        await session.commit()


async def consume_bonus_count(user_id: int):
    async with async_session() as session:
        stmt = (update(User).where(User.user_id == user_id).values(bonus_count=User.bonus_count - 3))
        await session.execute(stmt)
        await session.commit()



async def remove_user_premium(user_id ):
    async with async_session() as session:
        stmt = (update(User).where(User.user_id == user_id).values(premium=False, vip_expiry=None , pgender ='U'))
        await session.execute(stmt)
        await session.commit()


async def ban_user(user_id: int, days: int):
    async with async_session() as session:
        ban_expiry_date = datetime.datetime.now() + datetime.timedelta(days=days)
        stmt = update(User).where(User.user_id == user_id).values(banned =True, ban_expiry=ban_expiry_date)
        await session.execute(stmt)
        await session.commit()  


async def unban_user(user_id: int) -> None:
    async with async_session() as session:
        stmt = update(User).where(User.user_id == user_id).values(banned=False, ban_expiry=None)
        await session.execute(stmt)
        await session.commit()





async def make_request_false(user_id: int) -> None:
    async with async_session() as session:
        stmt = update(User).where(User.user_id == user_id).values(request=False)
        await session.execute(stmt)
        await session.commit()





async def make_request_true(user_id: int) -> None:
    async with async_session() as session:
        stmt = update(User).where(User.user_id == user_id).values(request=True)
        await session.execute(stmt)
        await session.commit()



  


async def remove_previous_id(user_id: int) -> None:
    async with async_session() as session:
        stmt = update(User).where(User.user_id == user_id).values(previous_id=None)
        await session.execute(stmt)
        await session.commit()



async def get_users_count_with_low_chat_count(count):
    async with session_pool() as session:
        query = select(func.count(User.user_id)).where(User.chat_count >= count)
        result = await session.execute(query)
        return result.scalar()


async def create_match(user_id, partner_id):
    async with async_session() as session:
        # Use the update statement to set the partner_id for the given user_id
        update_stmt1 = (update(User).where(User.user_id == user_id).values(partner_id=partner_id , request =False))
        update_stmt2 = (update(User).where(User.user_id == partner_id).values(partner_id=user_id , request=False))
        await session.execute(update_stmt1)
        await session.execute(update_stmt2)
        await session.commit()
        await session.close()


async def get_all_count():
    async with async_session() as session:
        result = await session.execute(func.count(User.user_id))
        return result.scalar()


async def get_all_vip_users():
    async with async_session() as session:
        query = select(User).where(User.premium == True )
        result = await session.execute(query)
        vip_users = result.scalars().all()
        return [user for user in vip_users]



async def get_all_u_users():
    async with async_session() as session:
        query = select(User).where((User.partner_id != None) & (User.gender == "U"))
        result = await session.execute(query)
        u_users = result.scalars().all()
        return u_users



async def get_users_by_gender(gender):
    async with async_session() as session:
        query = select(User).where(User.gender == gender )
        result = await session.execute(query)
        vip_users = result.scalars().all()
        return [user for user in vip_users]



async def get_male_user():
    async with async_session() as session:
        query = select(User).where((User.premium == False) & (User.gender == "M"))
        result = await session.execute(query)
        vip_users = result.scalars().all()
        return [user for user in vip_users]



async def get_vip_user():
    async with async_session() as session:
        query = select(User).where(User.premium == True )
        result = await session.execute(query)
        vip_users = result.scalars().all()
        return [user for user in vip_users]



async def get_users_count_by_gender(gender):
    async with async_session() as session:
        query = select(func.count(User.user_id)).where(User.gender == gender)
        result = await session.execute(query)
        return result.scalar()




async def get_vips_count():
    async with async_session() as session:
        query = select(func.count(User.user_id)).where(User.premium == True)
        result = await session.execute(query)
        return result.scalar()





async def get_bans_count():
    async with async_session() as session:
        query = select(func.count(User.user_id)).where(User.banned == True)
        result = await session.execute(query)
        return result.scalar()




async def get_users_count_with_low_chat_count(count):
    async with async_session() as session:
        query = select(func.count(User.user_id)).where(User.chat_count >= count)
        result = await session.execute(query)
        return result.scalar()

async def get_all_user_ids():
    async with async_session() as session:
        stmt = select(User.user_id)
        result = await session.execute(stmt)
        user_ids = [row[0] for row in result.fetchall()]
        return user_ids




import asyncio


async def get_match(user_id, gender, pgender ,previous_id):
    async with async_session() as session:
        result = await session.execute(func.count(Queue.user_id))
       

        if result.scalar()< 6:
            return None

        if pgender != "U":
            query = (
                select(Queue.user_id)
                .join(User, Queue.user_id == User.user_id)
                .filter(Queue.user_id != user_id)
                .filter(Queue.user_id != previous_id)
                .filter(User.gender == pgender)
                .filter(User.pgender.in_([pgender, "U"]))
                .order_by(asc(Queue.created_at))
            )
        else:
            print(f" Else  U PART ")
            if gender == "M":
                print(f" Else  m part    ++> {gender} {pgender}")
                query = (
                    select(Queue.user_id)
                    .join(User, Queue.user_id == User.user_id)
                    .filter(Queue.user_id != user_id)
                    .filter(Queue.user_id != previous_id)
                    .filter(User.pgender.in_([gender, "U"]))
                    .order_by(asc(Queue.created_at))
                )
            elif gender == "F":
                print(f" Else  f part    ++> {gender} {pgender}")
                query = (
                    select(Queue.user_id)
                    .join(User, Queue.user_id == User.user_id)
                    .filter(Queue.user_id != user_id)
                    .filter(Queue.user_id != previous_id)

                    .filter(User.pgender.in_([gender, "U"]))
                    .order_by(asc(Queue.created_at))
                )
            else:
                print(f" Else  u part    ++> {gender} {pgender}")
                query = (
                    select(Queue.user_id)
                    .join(User, Queue.user_id == User.user_id)
                    .filter(Queue.user_id != user_id)
                    .filter(Queue.user_id != previous_id)
                    .filter(User.pgender == pgender)
                    .order_by(asc(Queue.created_at))
                )

        result = await session.execute(query)

        return result.scalar()
