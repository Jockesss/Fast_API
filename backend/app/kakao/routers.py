import logging
import os
import httpx

from fastapi import APIRouter, HTTPException
from mongo.connectMongo import connect_mongo
from kakao.models import Address, Addresses
from fastapi.responses import JSONResponse
from bson import ObjectId

api_key = os.getenv("API_KEY")
router = APIRouter()
logger = logging.getLogger(__name__)

db = connect_mongo()
fire_stations_collection = db['fire_stations_new']
hospitals_collection = db['hospitals']


def query_addresses(collection, address):
    query = {}
    if address.sd:
        query["sd"] = address.sd
    if address.sgg:
        query["sgg"] = address.sgg
    if address.umd:
        query["umd"] = address.umd

    result = collection.find(query)

    results_list = [dict(item, _id=str(item["_id"])) for item in result]
    return results_list


@router.post("/geolocation/address/fire_stations", response_model=list[Addresses])
async def get_fire_stations(address: Address):
    results = query_addresses(fire_stations_collection, address)
    return results


@router.post("/geolocation/address/hospitals", response_model=list[Addresses])
async def get_hospitals(address: Address):
    results = query_addresses(hospitals_collection, address)
    return results


@router.get("/geolocation/coordinates")
async def get_geolocation_by_coordinates(sd: str, sgg: str, umd: str):
    address = f"{sd} {sgg} {umd}"
    url = f"https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            print(response.status_code)

            data = response.json()
            print(data)
            # documents = data.get("documents", [])
            # print(documents)
            # logger.info(f"Kakao Maps API response: {documents}")

            if data["documents"]:
                coordinates = data["documents"][0]["address"]
                return {"latitude": coordinates["y"], "longitude": coordinates["x"]}
            else:
                raise HTTPException(status_code=404, detail="No geolocation data found")

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
