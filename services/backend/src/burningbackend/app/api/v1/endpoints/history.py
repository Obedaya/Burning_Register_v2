from burningbackend.app.models.history import History

from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()

@router.get("/", response_description="History retrieved")
async def get_history(movie: str = None) -> list[History]:
    if movie is None:
        history = await History.all().to_list()
        return history
    else:
        history = await History.find({"movie": movie}).to_list()
        return history

@router.post("/", response_description="History Item added to the database")
async def add_history(history: History) -> dict:
    await history.create()
    history = await History.find_one({"timestamp": history.timestamp})
    return {"message": "History added successfully", "data": history}

@router.post("/cancel/", response_description="Canceled booked order")
async def add_history(_id: str, iscancled: bool = True) -> dict:
    history = await History.get(_id)
    if not history:
        raise HTTPException(
            status_code=404,
            detail="History record not found"
        )
    history.iscancled = iscancled
    await history.save()
    return {"message": "History updated successfully", "data": history}

# Get total of all not cancelled histories for specific movie
@router.get("/total", response_description="Total of all histories for specific movie")
async def get_total(movie: str, isteam: bool = False, cancellation: bool = False, pfand: bool = True) -> float:
    if cancellation is False:
        if isteam is True:
            history = await History.find({"movie": movie, "cancellation": False, "isteam": True}).to_list()
        else:
            history = await History.find({"movie": movie, "cancellation": False}).to_list()
    else:
        history = await History.find({"movie": movie, "cancellation": True}).to_list()
    total = 0
    for i in history:
        total += i.total
    if pfand is False:
        for i in history:
            for j in i.products:
                if j.name == "Pfand":
                    total -= j.price * j.amount
    return float(total)

# Get total amount of Tickets sold for specific movie
@router.get("/tickets", response_description="Total of all tickets for specific movie")
async def get_tickets(movie: str, isteam: bool = False, freeticket: bool = False) -> int:
    if isteam is True:
        history = await History.find({"movie": movie, "cancellation": False, "isteam": True}).to_list()
    else:
        history = await History.find({"movie": movie, "cancellation": False, "isteam": False}).to_list()
    total = 0
    for i in history:
        for j in i.products:
            if freeticket is False:
                if j.name == "Ticket":
                    total += j.amount
            else:
                if j.name == "Freiticket":
                    total += j.amount
    return total