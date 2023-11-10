from burningbackend.app.models.reservation import Reservation

from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


@router.get("/reservations", response_description="Reservations retrieved")
async def get_all_reservations() -> Reservation:
    reservations = await Reservation.all().to_list()
    if not reservations:
        raise HTTPException(status_code=404, detail="No reservations found")
    return reservations


@router.post("/reservation/add", response_description="Reservation added to the database")
async def add_reservation(reservation: Reservation) -> dict:
    await reservation.create()
    reservation = await Reservation.find_one({"timestamp": reservation.timestamp})
    return {"message": "Reservation added successfully", "data": reservation}


@router.put("/reservation/update/{id}", response_description="Reservation updated in the database")
async def update_reservation(id: str, reservation: Reservation) -> dict:
    req = {k: v for k, v in req.dict().items() if v is not None}
    update_query = {"$set": {field: value for field, value in req.items()}}
    reservation = await Reservation.get(id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Movie record not found")
    updated_movie = await reservation.update(update_query)
    return {"message": "Reservation updated successfully", "data": updated_movie}


@router.post("/reservation/scan/{id}", response_description="Reservation scanned")
async def scan_reservation(id: str) -> dict:
    reservation = await Reservation.get(id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation record not found")
    
    if reservation.scanned == True:
        raise HTTPException(status_code=400, detail="Reservation already scanned")
    
    await reservation.update({"$set": {"scanned": True}})

    return {"message": "Reservation scanned successfully", "data": reservation}