import sqlalchemy
from src import database as db

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_barrels(barrels_delivered: list[Barrel], order_id: int):
    """ """
    print(f"barrels delivered: {barrels_delivered} order_id: {order_id}")

    #500ml for small barrels (from logs)
    totalml = barrels_delivered * 500
    #100 gold for small barrels (from logs)
    totalgold = barrels_delivered * 100

    #add how many ml you just bought
    updateml = f"UPDATE global_inventory SET num_green_ml = (num_green_ml + {totalml})"
    #take away how much gold you just spent
    updategold = f"UPDATE global_inventory SET gold = (gold - {totalgold})"

    #buy 500ml barrels
    #use update
    with db.engine.begin() as connection:
        resultml = connection.execute(sqlalchemy.text(updateml))
        resultgold = connection.execute(sqlalchemy.text(updategold))
        
    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(wholesale_catalog)

    #sql statements as strings
    greenpotionqry = "SELECT num_green_potions FROM global_inventory"
    goldqry = "SELECT gold FROM global_inventory"
    mlqry = "SELECT num_green_ml FROM global_inventory"

    #still need to do the >= 10 stuff idk
    with db.engine.begin() as connection:
        greenpotion = connection.execute(sqlalchemy.text(greenpotionqry)).scalar()
        goldamt = connection.execute(sqlalchemy.text(goldqry)).scalar()
        mlamt = connection.execute(sqlalchemy.text(mlqry)).scalar()
        
    return [
        {
            "sku": "SMALL_GREEN_BARREL",
            "quantity": 1,
        }
    ]

