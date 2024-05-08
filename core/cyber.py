import datetime

from core.utils.web3_utils import Web3Utils
from fake_useragent import UserAgent
import aiohttp


class Cyber:
    def __init__(self, key: str, proxy: str):
        self.web3_utils = Web3Utils(key=key)
        self.proxy = f"http://{proxy}" if proxy is not None else None

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': 'Bearer null',
            'Content-Type': 'application/json',
            'Origin': 'https://alienxchain.io',
            'Referer': 'https://alienxchain.io/airdrop',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Source': 'web',
            'User-Agent': UserAgent(os='windows').random,
        }

        self.session = aiohttp.ClientSession(
            headers=headers,
            trust_env=True
        )
        self.url = 'https://api.cyberconnect.dev/l2/'

    async def get_nonce(self):
        json_data = {
            "operationName": "getNonce",
            "query": "mutation getNonce($input: NonceInput!) {\n nonce(input: $input) {\n status\n message\n data\n }\n}\n",
            "variables": {
                "input": {
                    "address": self.web3_utils.acct.address
                }
            }
        }

        response = await self.session.post(url=self.url, json=json_data, proxy=self.proxy)
        return (await response.json()).get('data').get('nonce').get('data')

    async def login(self):
        nonce = await self.get_nonce()
        issued_at = datetime.datetime.utcnow().isoformat() + "Z"
        signed_message = f"cyber.co wants you to sign in with your Ethereum account:\n{self.web3_utils.acct.address}\n\nSign in Cyber\n\nURI: https://cyber.co\nVersion: 1\nChain ID: 56\nNonce: {nonce}\nIssued At: {issued_at}"
        signature = self.web3_utils.get_signed_code(signed_message)

        json_data = {
            'operationName': "login",
            'query': "mutation login($input: LoginInput!) {\n  login(input: $input) {\n    status\n    message\n    data {\n      accessToken\n      address\n    }\n  }\n}\n",
            'variables': {
                "input": {
                    "signedMessage": signed_message,
                    "signature": signature,
                    "address": self.web3_utils.acct.address,
                    "chainId": 56
                }
            }
        }

        response = await self.session.post(url=self.url, json=json_data, proxy=self.proxy)
        auth_token = (await response.json()).get('data').get('login').get('data').get('accessToken')
        self.session.headers["Authorization"] = f"{auth_token}"
        return True if (await response.json()).get('data').get('login').get('status') == 'SUCCESS' else False

    async def checkin(self):
        json_data = {
            'operationName': "checkedIn",
            'query': "mutation checkedIn {\n  checkIn {\n    status\n  }\n}\n",
            'variables': {}
        }

        response = await self.session.post(url=self.url, json=json_data, proxy=self.proxy)
        return True if (await response.json()).get('data').get('checkIn').get('status') == 'SUCCESS' else False

    async def logout(self):
        await self.session.close()
