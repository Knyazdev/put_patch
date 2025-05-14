from fastapi import FastAPI
import uvicorn
from time import sleep, time
from asyncio import sleep as i_sleep
import threading

app = FastAPI()


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync: threads -> {threading.active_count()}")
    print(f"sync. Started {id}: {time():.2f}")
    sleep(3)
    print(f"sync. Ended {id}: {time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async: threads -> {threading.active_count()}")
    print(f"async. Started {id}: {time():.2f}")
    await i_sleep(3)
    print(f"async. Ended {id}: {time():.2f}")


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
