"""
Schémas Pydantic - Millésime Sans Frontières
Validation des données d'entrée et de sortie
"""

from app.schemas.base import BaseSchema, BaseResponse, PaginationParams, PaginatedResponse, ErrorResponse, SuccessResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, UserWithToken, UserProfile, PasswordChange, PasswordReset, PasswordResetConfirm
from app.schemas.barrel import BarrelCreate, BarrelUpdate, BarrelResponse, BarrelListResponse, BarrelFilter
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderItemCreate, OrderItemUpdate, OrderItemResponse, OrderListResponse, OrderFilter, OrderStatusUpdate, OrderSummary
from app.schemas.quote import QuoteCreate, QuoteUpdate, QuoteResponse, QuoteItemCreate, QuoteItemUpdate, QuoteItemResponse, QuoteListResponse, QuoteFilter, QuoteStatusUpdate, QuoteSend, QuoteSummary

__all__ = [
    "BaseSchema",
    "BaseResponse",
    "PaginationParams",
    "PaginatedResponse", 
    "ErrorResponse",
    "SuccessResponse",
    "UserCreate",
    "UserUpdate", 
    "UserResponse",
    "UserLogin",
    "UserWithToken",
    "UserProfile",
    "PasswordChange",
    "PasswordReset",
    "PasswordResetConfirm",
    "BarrelCreate",
    "BarrelUpdate",
    "BarrelResponse",
    "BarrelListResponse",
    "BarrelFilter",
    "OrderCreate",
    "OrderUpdate",
    "OrderResponse",
    "OrderItemCreate",
    "OrderItemUpdate",
    "OrderItemResponse",
    "OrderListResponse",
    "OrderFilter",
    "OrderStatusUpdate",
    "OrderSummary",
    "QuoteCreate",
    "QuoteUpdate",
    "QuoteResponse",
    "QuoteItemCreate",
    "QuoteItemUpdate",
    "QuoteItemResponse",
    "QuoteListResponse",
    "QuoteFilter",
    "QuoteStatusUpdate",
    "QuoteSend",
    "QuoteSummary"
]
