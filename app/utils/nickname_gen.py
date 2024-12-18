import random
from app.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

async def generate_nickname_with_id(session: Optional[AsyncSession] = None, user_id: str = "default_user_id") -> str:
    """
    Generate a URL-safe nickname using adjectives, animal names, and append the user ID if necessary.
    Ensures uniqueness if a database session is provided.
    """
    adjectives = ["quick", "happy", "fearless", "sneaky", "kind"]
    animals = ["tiger", "owl", "badger", "kangaroo", "wolf"]

    base_nickname = f"{random.choice(adjectives)}{random.choice(animals)}{random.randint(0, 999)}"
    unique_nickname = base_nickname

    if session:
        retries = 0
        max_retries = 10  # Limit the number of retries to ensure no infinite loop

        while retries < max_retries:
            # Check if the nickname already exists
            result = await session.execute(select(User).filter_by(nickname=unique_nickname))
            existing_user = result.scalar()

            if not existing_user:
                break  # Nickname is unique

            # Append the user_id and try again
            unique_nickname = f"{base_nickname}_{user_id}"
            retries += 1

        if retries == max_retries:
            raise ValueError("Unable to generate a unique nickname after several retries.")

    return unique_nickname