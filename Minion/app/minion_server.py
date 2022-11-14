import hashlib
import os
import aiohttp
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class MinionData(BaseModel):
    """Class that represent minion server with passwords range and hashes to compare."""

    min_range: int
    max_range: int
    hashes: List[str]


class MinionSub(BaseModel):
    """Class that represent minion server connection.
    """

    url: str
    port: int

    def encode(self):
        """Return object of type dict."""

        return self.__dict__
    

@app.on_event("startup")
async def startup_event():
    """Create connection to master server on startup.
    """
    async with aiohttp.ClientSession() as session:
        await subscribe_to_master(f'http://{os.getenv("MASTER_HOST")}:8000', session)


@app.post("/api/crack-hashes-in-range/")
async def crack_hashes(data: MinionData):
    """Post method receving MinionData object

    Loops over range of passwords calculate their MD5 hashes and compare with the given hashes.
    """

    try:
        # Create hash dict to optimize hash comparing to average O(1)
        hash_dict = dict.fromkeys(data.hashes)

        # Result dictionary where key is the hash and value is the password
        result_dict = {}
        minion_url = f'http://{os.getenv("HOST_NAME")}:{int(os.getenv("APP_PORT"))}'

        for i in range(data.min_range, data.max_range + 1):
            phone_number = get_phone_number(str(i))
            hash = hashlib.md5(phone_number.encode()).hexdigest()

            if hash in hash_dict:
                print(f"Found match! {phone_number} \n")
                result_dict[hash] = phone_number
            
        return {"Host": minion_url,
                "Status": "Success",
                "Cracked_passwords": result_dict}

    except Exception as e:
        result_dict["Status"] = "Failed"

        return {"Host": minion_url,
                "Status": "Failed",
                "Exception": e}


def get_phone_number(num: str) -> str:
    """Returns given number as phone number - add zeros to prefix when needed."""
    
    prefix = "05" + "0" * (8 - len(num))
    
    return prefix + num


async def subscribe_to_master(master_url: str, session: aiohttp.ClientSession):
    try:
        minion_sub = MinionSub(url=f'http://{os.getenv("HOST_NAME")}', port=int(os.getenv("APP_PORT")))
        url = master_url + "/api/subscribe/"

        async with session.post(url=url, json=minion_sub.encode()) as response:
            resp = await response.json()
            print(f"Successfully subscribed {minion_sub.url} to Master.")

            return resp

    except Exception as e:
        print(f"Unable to subscribe url {minion_sub.url} due to {e}.")

