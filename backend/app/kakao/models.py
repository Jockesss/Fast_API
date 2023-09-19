from pydantic import BaseModel


class Address(BaseModel):
    sd: str
    sgg: str
    umd: str


class Addresses(BaseModel):
    id_address: str
    sd: str
    sgg: str
    umd: str
    num: str
    place_name: str
    phone: str
    x: str
    y: str
