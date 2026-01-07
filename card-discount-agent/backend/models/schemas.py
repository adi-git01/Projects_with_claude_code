"""
Pydantic models for request/response schemas
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class CreditCard(BaseModel):
    """Credit card model"""
    id: str
    name: str
    bank: str
    type: Literal['reward_points', 'cashback', 'instant_discount']
    base_reward: float
    color: str

class Platform(BaseModel):
    """Shopping platform model"""
    name: str
    type: Literal['ecommerce', 'quickcommerce']
    url: str

class Discount(BaseModel):
    """Discount/offer model"""
    type: Literal['instant', 'cashback', 'coupon', 'reward_points']
    value: float
    is_percentage: bool
    max_cap: Optional[float] = None
    min_purchase: Optional[float] = None
    description: str
    card_required: Optional[str] = None
    valid_until: Optional[str] = None

class ProductDeal(BaseModel):
    """Product deal with all price breakdowns"""
    platform: Platform
    product_name: str
    product_url: str
    base_price: float
    delivery_charge: float = 0
    available_discounts: List[Discount] = []
    effective_price: float
    best_card: Optional[CreditCard] = None
    savings: float = 0
    is_best_deal: bool = False
    in_stock: bool = True

class SearchRequest(BaseModel):
    """Search request from frontend"""
    query: str = Field(..., description="Product URL or name")
    selected_cards: List[str] = Field(..., description="List of card IDs to consider")

class SearchProgress(BaseModel):
    """Search progress status"""
    step: str
    status: Literal['pending', 'in_progress', 'completed', 'error']
    message: str

class SearchResponse(BaseModel):
    """Search response with deals"""
    product_name: str
    product_image: Optional[str] = None
    deals: List[ProductDeal]
    search_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    progress: List[SearchProgress] = []

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
