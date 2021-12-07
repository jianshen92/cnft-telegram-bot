from typing import List

import requests

from tbot.model import CNFTlisting


def extract_data(data: dict) -> CNFTlisting:
    listing = CNFTlisting(
        listing_id=data["_id"],
        asset_id=data["asset"]["assetId"],
        price_lovelace=data["price"],
    )
    return listing


def get_price_data(project: str, query: str) -> List[CNFTlisting]:
    headers = {
        "authority": "api.cnft.io",
        "accept": "application/json, text/plain, */*",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        ),
        "content-type": "application/json",
        "sec-gpc": "1",
        "origin": "https://cnft.io",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://cnft.io/",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    http_data = (
        '{"nsfw":false,"page":1'
        f',"project":"{project}"'
        f',"search":"{query}"'
        ',"sold":false,"sort":{"price":1},"verified":true,"types":["offer","listing"]}'
    )

    response = requests.post(
        "https://api.cnft.io/market/listings", headers=headers, data=http_data
    )

    if response.status_code != 200:
        print(response.text)
        raise Exception("Http response not 200")
    try:
        response_data = response.json()
    except Exception as e:
        print(e)

    final_data = []
    for data in response_data["results"]:
        listing = extract_data(data)
        final_data.append(listing)

    return final_data


def format_message(market_data: List[CNFTlisting]) -> str:
    return "\n".join([item.md_v2_serialize() for item in market_data])


def replace_dash(query: str) -> str:
    return query.replace("-", " ")
