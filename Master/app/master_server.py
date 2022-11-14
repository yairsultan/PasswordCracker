import asyncio
import time
import aiohttp
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
minions = []
hashes = open('hashes.txt').read().splitlines()


class MinionData(BaseModel):
    """Class that represent minion server with passwords range and hashes to compare."""

    min_range: int
    max_range: int
    hashes: List[str]

    def encode(self):
        """Return object of type dict."""

        return self.__dict__


class MinionSub(BaseModel):
    """Class that represent minion server connection.
    """

    url: str
    port: int


@app.get("/api/crack-hashes/")
async def crack_hashes():
    """Return cracked hashes passwords

    Seperate the work between serveral servers to achieve better performance.
    """

    start = time.time()
    minions_data = even_intervals_minions((10 ** 8) - 1, len(minions))

    async with aiohttp.ClientSession() as session:
        tasks = [post(url, session, data) for url, data in zip(minions, minions_data)]
        ret = await asyncio.gather(*tasks, return_exceptions=True)

    print(f"Finalized all. Return is a list of len {len(ret)} outputs.\nResult: {ret}")
    print(f"\n\nTotal time is: {time.time()-start}\n")

    return ret


@app.post("/api/subscribe/", status_code=201)
async def subscribe_minion(data: MinionSub):
    """Subscribe minion server to the master.
    """

    minions.append(f"{data.url}:{data.port}")
    print(minions)
    print(f"New minion {data.url} has subscribed to master!")


async def post(url: str, session: aiohttp.ClientSession, body: MinionData):
    """Post a single request

    Return json with Host, Status and Cracked_hashes dict.
    """

    try:
        async with session.post(url=url + "/api/crack-hashes-in-range/", json=body.encode()) as response:
            resp = await response.json()
            print(f"Successfully got url {url} with res: {resp}.")

            return resp

    except Exception as e:
        print(f"Unable to get url {url} due to {e}.")
        
        return {"Host": url, "Status": "Failed", "Exception": e}


def even_intervals_minions(value: int, n: int) -> List[MinionData]:
    """Generate MinionData objects and initialize them with even interval ranges.
    """

    minions = []
    bin_size = (value + 1) // n

    for x in range (n):
        minions.append(MinionData(min_range=x * bin_size, max_range=(x + 1) * bin_size - 1, hashes=hashes))

    # In case we have uneven intervals we add the reminder to the last range
    minions[n - 1].max_range = 99999999
        
    return minions
