import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from apartment_service import ApartmentService
from payment_service import PaymentService


class Apartment(BaseModel):
    property_id: int
    unit: Optional[int] = None


class Property(BaseModel):
    manager_id: int
    name: Optional[str] = None
    address: str


class Tenant(BaseModel):
    apartment_id: int
    name: str
    date_of_birth: Optional[str] = None
    encrypted_ssn: str
    is_primary: int


class Payment(BaseModel):
    tenant_id: str
    date_str: str
    amount: float


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://www.lymanscribbage.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apartment service
#
# (in the interest of time, two APIs are expressed in the same service).  The "Apartment"
# service includes CRU methods for apartments, properties, tenants.


# noinspection PyUnusedLocal
@app.get("/apartments/{apartment_id}")
async def get_apartment(apartment_id: int):
    return ApartmentService.get_dev_service().get_apartment(apartment_id)


# noinspection PyUnusedLocal
@app.post("/apartments")
async def add_apartment(apartment: Apartment):
    # noinspection PyUnusedLocal
    pass


# noinspection PyUnusedLocal
@app.put("/apartments/{apartment_id}")
async def update_apartment(apartment_id: int, apartment: Apartment):
    pass


# noinspection PyUnusedLocal
@app.get("/properties/{property_id}")
async def get_property(property_id: int):
    return ApartmentService.get_dev_service().get_property(property_id)


# noinspection PyUnusedLocal
@app.post("/properties")
async def add_property(property_obj: Property):
    # noinspection PyUnusedLocal
    pass


# noinspection PyUnusedLocal
@app.put("/properties/{property_id}")
async def update_apartment(property_id: int, property_obj: Property):
    pass


# noinspection PyUnusedLocal
@app.get("/tenants/{tenant_id}")
async def get_tenant(tenant_id: int):
    return ApartmentService.get_dev_service().get_tenant(tenant_id)


# noinspection PyUnusedLocal
@app.post("/tenants")
async def add_tenant(tenant: Tenant):
    # noinspection PyUnusedLocal
    pass


# noinspection PyUnusedLocal
@app.put("/tenants/{tenant_id}")
async def update_tenant(tenant_id: int, tenant: Tenant):
    pass

# Payment service


# noinspection PyUnusedLocal
@app.post("/tenants/{tenant_id}/payments")
async def add_payment(payment: Payment):
    # noinspection PyUnusedLocal
    return PaymentService.get_dev_service().add_payment()


# noinspection PyUnusedLocal
@app.get("/tenants/{tenant_id}/history")
async def get_payment_history(tenant_id: int):
    # noinspection PyUnusedLocal
    return PaymentService.get_dev_service().get_payment_history(tenant_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
