from pydantic import BaseModel


class CNFTlisting(BaseModel):
    listing_id: str
    asset_id: str
    price_lovelace: int

    @property
    def price_ada(self) -> int:
        return int(self.price_lovelace / 1000000)

    @property
    def url(self) -> str:
        return f"https://cnft.io/token/{self.listing_id}"

    def md_v2_serialize(self) -> str:
        return f"[{self.asset_id}]({self.url}) *{self.price_ada} ADA*"
