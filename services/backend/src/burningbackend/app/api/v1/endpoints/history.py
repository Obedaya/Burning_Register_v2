from burningbackend.app.models.history import History
from burningbackend.app.models.inventory import Inventory

from bson.objectid import ObjectId

from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


async def _update_inventory_for_order(products, reverse=False):
    """Update inventory amounts when an order is placed or cancelled.
    If reverse=True, restores inventory (for cancellations).
    """
    for product in products:
        inv_item = await Inventory.find_one({"name": product.name})
        if inv_item:
            if reverse:
                inv_item.amount += product.amount
                inv_item.amount_sold -= product.amount
            else:
                inv_item.amount -= product.amount
                inv_item.amount_sold += product.amount
            await inv_item.save()


@router.get("/", response_description="History retrieved")
async def get_history(movie: str = None, cancellation: bool = False) -> list[History]:
    if movie is None:
        if cancellation is False:
            history = await History.find({"cancellation": False}).to_list()
        else:
            history = await History.find({"cancellation": True}).to_list()
        return history
    else:
        if cancellation is False:
            history = await History.find({"movie": movie, "cancellation": False}).to_list()
        else:
            history = await History.find({"movie": movie, "cancellation": True}).to_list()
        return history


@router.post("/", response_description="History Item added to the database")
async def add_history(history: History) -> dict:
    await history.create()
    await _update_inventory_for_order(history.products, reverse=False)
    history = await History.find_one({"timestamp": history.timestamp})
    return {"message": "History added successfully", "data": history}


@router.post("/cancel/", response_description="Canceled booked order")
async def cancel_history(_id: str, cancellation: bool = True) -> dict:
    id = ObjectId(_id)
    history = await History.get(id)
    if not history:
        raise HTTPException(
            status_code=404,
            detail="History record not found"
        )
    if history.cancellation != cancellation:
        if cancellation:
            await _update_inventory_for_order(history.products, reverse=True)
        else:
            await _update_inventory_for_order(history.products, reverse=False)
    history.cancellation = cancellation
    await history.save()
    return {"message": "History updated successfully", "data": history}


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
                if j.name == "Ticket":
                    total += j.amount
                if j.name == "Freiticket":
                    total += j.amount
    return total
