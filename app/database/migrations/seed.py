from sqlmodel import Session
from app.database.models import Warehouse
from app.schemas import Address


def create_warehouses(engine):
    address_1 = Address(
        address_1="123 Main St", city="Springfield", state="IL", country="USA"
    )
    address_2 = Address(
        address_1="456 Elm St", city="Shelbyville", state="KY", country="USA"
    )
    warehouse_1 = Warehouse(name="Warehouse A", address=address_1, phone="813-555-1234")
    warehouse_2 = Warehouse(name="Warehouse B", address=address_2, phone="502-555-5678")
    with Session(engine) as session:
        session.add(warehouse_1)
        session.add(warehouse_2)

        session.commit()


# Create more seed functions here
