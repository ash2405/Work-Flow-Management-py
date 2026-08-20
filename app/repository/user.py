from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import User

# get user detail by id
async def get_user_by_id(
        db:AsyncSession,
        user_id:int
)->User:

    user = await db.execute(
        select(User)
        .options(
            selectinload(User.projects),
            selectinload(User.department)

        )
        .where(User.id == user_id)
    )

    return user.scalar_one_or_none()

# get all user
async def get_all_user(
        db:AsyncSession
)->list[User]:
    user_list = await db.execute(
        select(User).options(User.projects)
    )

    return list(user_list.scalars().all())

# get update user
async def update_user_detail(
        db:AsyncSession,
        data:User,
        user:User
)-> User:

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field , value in update_data.items():
        setattr(user,field, value)

    await db.commit()
    await db.refresh(user)

    return user

# user delete
async def delete_user(
    db: AsyncSession,
    user: User,
):   await db.delete(user)




# below is example query

# query = (
#     select(User)
#     .options(
#         selectinload(User.projects)
#         .options(
#             selectinload(Project.items)
#             .selectinload(Item.category),

#             selectinload(Project.groups)
#             .selectinload(Group.size),
#         ),

#         selectinload(User.location)
#         .selectinload(Location.city)
#         .selectinload(City.country),
#     )
# )