import os
import re
import requests

from concurrent.futures import ProcessPoolExecutor
from mongo.connectMongo import connect_mongo
from kakao.models import Addresses

api_key = os.getenv("API_KEY")

districts_busan = {
    "중구": [
        "영주동", "대창동1가", "대창동2가", "중앙동1가", "중앙동2가", "중앙동3가",
        "중앙동4가", "중앙동5가", "중앙동6가", "중앙동7가", "동광동1가", "동광동2가",
        "동광동3가", "동광동4가", "동광동5가", "대청동1가", "대청동2가", "대청동3가",
        "대청동4가", "보수동1가", "보수동2가", "보수동3가", "부평동1가", "부평동2가",
        "부평동3가", "부평동4가", "신창동1가", "신창동2가", "신창동3가", "신창동4가",
        "창선동1가", "창선동2가", "광복동1가", "광복동2가", "광복동3가", "남포동1가",
        "남포동2가", "남포동3가", "남포동4가", "남포동5가", "남포동6가"
    ],
    "서구": [
        "동대신동1가", "동대신동2가", "동대신동3가", "서대신동1가", "서대신동2가",
        "서대산동3가", "부용동1가", "부용동2가", "부민동1가", "부민동2가", "부민동3가",
        "토성동1가", "토성동2가", "토성동3가", "아미동1가", "아미동2가", "토성동4가",
        "토성동5가", "초장동", "충무동1가", "충무동2가", "충무동3가", "남부민동", "암남동"
    ],
    "동구": ["초량동", "수정동", "좌천동", "범일동"],
    "영도구": [
        "대교동1가", "대교동2가", "대평동1가", "대평동2가", "남항동1가", "남항동2가",
        "남항동3가", "영선동1가", "영선동2가", "영선동3가", "영선동4가", "신선동1가",
        "신선동2가", "신선동3가", "봉래동1가", "봉래동2가", "봉래동3가", "봉래동4가",
        "봉래동5가", "청학동", "동삼동"
    ],
    "부산진구": [
        "양정동", "전포동", "부전동", "범천동", "범전동", "연지동", "초읍동", "부암동",
        "당감동", "가야동", "개금동"
    ],
    "동래구": [
        "명장동", "안락동", "칠산동", "낙민동", "복천동", "수안동", "명륜동", "온천동",
        "사직동"
    ],
    "남구": ["대연동", "용호동", "용당동", "문현동", "우암동", "감만동"],
    "북구": ["금곡동", "화명동", "만덕동", "덕천동", "구포동"],
    "해운대구": [
        "반송동", "석대동", "반여동", "재송동", "우동", "중동", "좌동", "송정동"
    ],
    "사하구": [
        "괴정동", "당리동", "하단동", "신평동", "장림동", "다대동", "구평동", "감천동"
    ],
    "금정구": [
        "두구동", "노포동", "청룡동", "남산동", "선동", "오륜동", "구서동", "장전동",
        "부곡동", "서동", "금사동", "회동동", "금성동"
    ],
    "강서구": [
        "대저1동", "대저2동", "강동동", "명지동", "죽림동", "식만동", "죽동동", "봉림동",
        "송정동", "화전동", "녹산동", "생곡동", "구랑동", "지사동", "미음동", "범방동",
        "신호동", "동선동", "성북동", "눌차동", "천성동", "대항동"
    ],
    "연제구": ["거제동", "연산동"],
    "수영구": ["망미동", "수영동", "민락동", "광안동", "남천동"],
    "사상구": ["삼락동", "모라동", "덕포동", "괘"],
    "기장군": [
        "기장읍", "장안읍", "정관읍", "일광읍", "철마면"
    ]
}

districts_kn = ["창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군",
                "함양군", "거창군", "합천군"]

specialties = ["병원", "가정의학과", "내과", "노인,요양병원", "대학병원", "비뇨기과", "산부인과", "성장클리닉", "성형외과", "소아청소년과", "시도립병원", "신경과",
               "신경외과", "안과", "영상의학과", "외과", "응급실", "의료센터", "이비인후과", "일반의원", "재활의학과", "정신건강의학과", "정형외과", "종합병원", "치과",
               "통증클리닉", "피부과", "한방병원", "한의원", "항문외과", "병원부속시설", "위탁의료기관", "선별진료소", "류마티스내과", "산부인과", "산후조리원", "심장내과",
               "내분비내과", "정신과"]


# Func info
def get_specialty_data(query, specialty, page):
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={query} {specialty}&page={page}'
    headers = {'Authorization': f'KakaoAK {api_key}'}
    response = requests.get(url, headers=headers)
    data = response.json()
    doc = data.get('documents', [])
    return doc


def get_hell_data(query):
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={query}'
    headers = {'Authorization': f'KakaoAK {api_key}'}
    response = requests.get(url, headers=headers)
    data = response.json()
    doc = data.get('documents', [])
    return doc


# Connect MongoDB
db = connect_mongo()
collection = db['fire_stations']


# id from MongoDB
def get_existing_ids():
    existing_ids = set()
    for station in collection.find({}, {'_id': 0, 'id': 1}):
        existing_ids.add(station['id'])
    return existing_ids


# Function check all streets
def process_pages_for_street(query, specialty, start_page, end_page):
    existing_ids = get_existing_ids()
    for page in range(start_page, end_page + 1):
        hospital = get_specialty_data(query, specialty, page)
        for station in hospital:
            station_id = station.get('id', '')
            if station_id not in existing_ids:
                collection.insert_one(station)
                existing_ids.add(station_id)
                print(f"Add in database: {station['place_name']} - {station['category_name']} - {station_id}")
            else:
                print(f"Duplicate: {station['place_name']} - {station['category_name']} - {station_id}")


# ADD HOSPITALS IN DATABASE
def get_hospital_busan(start_page, end_page):
    with ProcessPoolExecutor(max_workers=4) as executor:
        for region, subregions in districts_busan.items():
            for subregion in subregions:
                for specialty in specialties:
                    query = f'부산 {region} {subregion} {specialty}'
                    executor.submit(process_pages_for_street, query, specialty, start_page, end_page)


def get_hospital_kn(start_page, end_page):
    with ProcessPoolExecutor(max_workers=6) as executor:
        for region in districts_kn:
            for specialty in specialties:
                query = f'경상남도 {region} {specialty}'
                executor.submit(process_pages_for_street, query, specialty, start_page, end_page)


# ADD FIRE STATIONS IN DATABASE

def get_fire_station_kn(start_page, end_page):
    with ProcessPoolExecutor(max_workers=5) as executor:
        for region in districts_kn:
            query = f'경남 {region}'
            executor.submit(process_pages_for_street, query, "소방서", start_page, end_page)


def get_fire_station_busan(start_page, end_page):
    with ProcessPoolExecutor(max_workers=5) as executor:
        for region, subregions in districts_busan.items():
            for subregion in subregions:
                query = f'부산 {region} {subregion}'
                executor.submit(process_pages_for_street, query, "소방서", start_page, end_page)


# CLEAN DATABASE
def remove_duplicates_by_id(coll):
    unique_ids = set()
    documents_to_remove = []

    for document in coll.find():
        doc_id = document.get('id')
        if doc_id in unique_ids:
            documents_to_remove.append(document)
        else:
            unique_ids.add(doc_id)
    for document in documents_to_remove:
        coll.delete_one({'_id': document['_id']})

    print(f"Delete {len(documents_to_remove)} duplicate.")


def analyze_address(address):
    new_data_dict = {}
    address_parts = address.split()

    if len(address_parts) == 4:
        # Если адрес состоит из 4 слов, то первые два слова идут в sd и sgg, остальные в umd и num
        sd = address_parts[0]
        sgg = address_parts[1]
        umd = address_parts[2]
        num = address_parts[3]

        new_data_dict["sd"] = sd
        new_data_dict["sgg"] = sgg
        new_data_dict["umd"] = umd
        new_data_dict["num"] = num

    elif len(address_parts) == 5:
        # Если адрес состоит из 5 слов, то первые два слова идут в sd, остальные в sgg, umd и num
        sd = address_parts[0]
        sgg = address_parts[1]
        umd = address_parts[2] + " " + address_parts[3]
        num = address_parts[4]

        new_data_dict["sd"] = sd
        new_data_dict["sgg"] = sgg
        new_data_dict["umd"] = umd
        new_data_dict["num"] = num

    elif len(address_parts) == 6:
        sd = address_parts[0]
        sgg = address_parts[1] + " " + address_parts[2]
        umd = address_parts[3] + " " + address_parts[4]
        num = address_parts[5]

        new_data_dict["sd"] = sd
        new_data_dict["sgg"] = sgg
        new_data_dict["umd"] = umd
        new_data_dict["num"] = num

    return new_data_dict


def check_data():
    new_collection = db['fire_stations_new']
    results = collection.find()

    for document in results:
        address_name = document.get("address_name")
        place_name = document.get("place_name")

        # Анализируем адрес
        address_data = analyze_address(address_name)

        if address_data:
            # Создаем экземпляр Addresses
            new_data = Addresses(id_address=document.get("id"), place_name=place_name, phone=document.get("phone"),
                                 x=document.get("x"),
                                 y=document.get("y"), **address_data)

            # Добавляем в базу данных
            new_collection.insert_one(new_data.dict())
        else:
            print(address_name, "ERROR")
            print("Не удалось проанализировать адрес.")


if __name__ == '__main__':
    check_data()
    # START FOR HOSPITAL
    # get_hospital_busan(1, 3)
    # get_hospital_kn(1, 3)
    # START FOR FIRE STATION
    # get_fire_station_busan(1, 3)
    # get_fire_station_kn(1, 3)
    # remove_duplicates_by_id(collection)
