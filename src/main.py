
import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path
# isort: off
from api.hotels import router as router_hotels
from api.auth import router as router_auth
from api.rooms import router as router_rooms
# isort: on
sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
