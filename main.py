from core.cyber import Cyber
from core.utils.file_func import random_line
from loguru import logger
import asyncio


async def start(thread):
    logger.info(f"Поток {thread} | Начал работу")
    while True:
        acct = await random_line('data/private_keys.txt')
        if not acct: break

        if '::' in acct:
            private_key, proxy = acct.split('::')
        else:
            private_key = acct
            proxy = None

        cyber = Cyber(key=private_key, proxy=proxy)
        if await cyber.login():
            # logger.info(f"Поток {thread} | Адрес: {cyber.web3_utils.acct.address} | залогинился")
            if await cyber.checkin():
                logger.success(f"Поток {thread} | Адрес: {cyber.web3_utils.acct.address} | + 0.1%")
            else:
                logger.warning(f"Поток {thread} | Адрес: {cyber.web3_utils.acct.address} | сегодня уже получил 0.1%")
        else:
            logger.error(f"Поток {thread} | Адрес: {cyber.web3_utils.acct.address} | не смог залогиниться")

        await cyber.logout()
    logger.info(f"Поток {thread} | Закончил работу")


async def main():
    print("Автор софта: https://t.me/enigmo_crypto")

    thread_count = int(input("Введите кол-во потоков: "))
    # thread_count = 1
    tasks = []
    for thread in range(1, thread_count+1):
        tasks.append(asyncio.create_task(start(thread)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
