import asyncio
import random


async def random_line(filepath: str, delete: bool = True):
    with open(filepath, 'r') as file:
        keys = file.readlines()

    if not keys:
        return False
    random_key = random.choice(keys)
    if delete:
        keys.remove(random_key)

        with open(filepath, 'w') as file:
            file.writelines(keys)

    return random_key.strip()


async def first_line(filepath: str, delete: bool = True):
    with open(filepath, 'r') as file:
        keys = file.readlines()

    if not keys:
        return False
    first_key = keys[0]
    if delete:
        del keys[0]

        with open(filepath, 'w') as file:
            file.writelines(keys)

    return first_key.strip()
