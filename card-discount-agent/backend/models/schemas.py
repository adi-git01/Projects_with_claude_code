"""
Pydantic models for request/response schemas
Fixed to accept camelCase from frontend (JavaScript) while using snake_case internally (Python)
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CreditCard(BaseModel):
    """Credit card model"""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    bank: str
    type: Literal['reward_points', 'cashback', 'instant_discount']
    base_reward: float = Field(..., alias='baseReward')
    color: str

class Platform(BaseModel):
    """Shopping platform model"""
    name: str
    type: Optional[Literal['ecommerce', 'quickcommerce']] = 'ecommerce'  # Made optional for testing without search grounding
    url: Optional[str] = None  # Made optional for testing without search grounding

class Discount(BaseModel):
    """Discount/offer model"""
    model_config = ConfigDict(populate_by_name=True)

    type: Literal['instant', 'cashback', 'coupon', 'reward_points']
    value: float
    is_percentage: bool = Field(..., alias='isPercentage')
    max_cap: Optional[float] = Field(None, alias='maxCap')
    min_purchase: Optional[float] = Field(None, alias='minPurchase')
    description: str
    card_required: Optional[str] = Field(None, alias='cardRequired')
    valid_until: Optional[str] = Field(None, alias='validUntil')

class ProductDeal(BaseModel):
    """Product deal with all price breakdowns"""
    model_config = ConfigDict(populate_by_name=True, by_alias=True)

    platform: Platform
    product_name: str = Field(..., alias='productName')
    product_url: Optional[str] = Field(None, alias='productUrl')  # Made optional for testing without search grounding
    base_price: float = Field(..., alias='basePrice')
    delivery_charge: float = Field(0, alias='deliveryCharge')
    available_discounts: List[Discount] = Field([], alias='availableDiscounts')
    effective_price: float = Field(..., alias='effectivePrice')
    best_card: Optional[CreditCard] = Field(None, alias='bestCard')
    savings: float = 0
    is_best_deal: bool = Field(False, alias='isBestDeal')
    in_stock: bool = Field(True, alias='inStock')

class SearchRequest(BaseModel):
    """Search request from frontend"""
    model_config = ConfigDict(populate_by_name=True)

    query: str = Field(..., description="Product URL or name")
    selected_cards: List[str] = Field(..., alias='selectedCards', description="List of card IDs to consider")

class SearchProgress(BaseModel):
    """Search progress status"""
    step: str
    status: Literal['pending', 'in_progress', 'completed', 'error']
    message: str

class SearchResponse(BaseModel):
    """Search response with deals"""
    model_config = ConfigDict(populate_by_name=True, by_alias=True)

    product_name: str = Field(..., alias='productName')
    product_image: Optional[str] = Field(None, alias='productImage')
    deals: List[ProductDeal]
    search_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), alias='searchTimestamp')
    progress: List[SearchProgress] = []

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
