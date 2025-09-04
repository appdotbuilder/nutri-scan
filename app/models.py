from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal
from enum import Enum


# Enums for structured data
class NutriScore(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class HealthAssessment(str, Enum):
    GOOD = "Good for health"
    MODERATE = "Moderate"
    NOT_RECOMMENDED = "Not recommended"


# Persistent models (stored in database)
class FoodItem(SQLModel, table=True):
    """Food item with nutritional information and Nutri-score"""

    __tablename__ = "food_items"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, description="Food product name")
    brand: Optional[str] = Field(default=None, max_length=255, description="Brand name")
    description: Optional[str] = Field(default=None, max_length=1000, description="Product description")

    # Nutritional information (per 100g)
    energy_kj: Optional[Decimal] = Field(default=None, description="Energy in kJ per 100g")
    energy_kcal: Optional[Decimal] = Field(default=None, description="Energy in kcal per 100g")
    fat: Optional[Decimal] = Field(default=None, description="Fat content in grams per 100g")
    saturated_fat: Optional[Decimal] = Field(default=None, description="Saturated fat in grams per 100g")
    carbohydrates: Optional[Decimal] = Field(default=None, description="Carbohydrates in grams per 100g")
    sugars: Optional[Decimal] = Field(default=None, description="Sugars in grams per 100g")
    fiber: Optional[Decimal] = Field(default=None, description="Fiber in grams per 100g")
    protein: Optional[Decimal] = Field(default=None, description="Protein in grams per 100g")
    salt: Optional[Decimal] = Field(default=None, description="Salt in grams per 100g")
    sodium: Optional[Decimal] = Field(default=None, description="Sodium in grams per 100g")

    # Nutri-score and health assessment
    nutri_score: Optional[NutriScore] = Field(default=None, description="Nutri-score rating A-E")
    health_assessment: Optional[HealthAssessment] = Field(default=None, description="Health impact assessment")

    # Additional metadata
    ingredients: Optional[List[str]] = Field(default=None, sa_column=Column(JSON), description="List of ingredients")
    allergens: Optional[List[str]] = Field(default=None, sa_column=Column(JSON), description="List of allergens")
    categories: Optional[List[str]] = Field(default=None, sa_column=Column(JSON), description="Product categories")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    barcodes: List["Barcode"] = Relationship(back_populates="food_item")
    scan_history: List["ScanHistory"] = Relationship(back_populates="food_item")


class Barcode(SQLModel, table=True):
    """Barcode associated with food items"""

    __tablename__ = "barcodes"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, max_length=50, description="Barcode value (EAN-13, UPC, etc.)")
    barcode_type: str = Field(max_length=20, description="Type of barcode (EAN13, UPC, etc.)")
    food_item_id: int = Field(foreign_key="food_items.id")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    food_item: FoodItem = Relationship(back_populates="barcodes")


class ScanHistory(SQLModel, table=True):
    """History of barcode scans for analytics"""

    __tablename__ = "scan_history"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    food_item_id: int = Field(foreign_key="food_items.id")
    barcode_scanned: str = Field(max_length=50, description="The actual barcode that was scanned")
    scan_timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_agent: Optional[str] = Field(default=None, max_length=500, description="Browser/device info")
    ip_address: Optional[str] = Field(default=None, max_length=45, description="User IP address")

    # Relationships
    food_item: FoodItem = Relationship(back_populates="scan_history")


class NutritionProfile(SQLModel, table=True):
    """Predefined nutrition profiles for health assessment calculations"""

    __tablename__ = "nutrition_profiles"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, description="Profile name (e.g., 'General Adult', 'Low Sodium')")
    description: Optional[str] = Field(default=None, max_length=500)

    # Threshold values for health assessment
    max_fat_per_100g: Optional[Decimal] = Field(default=None, description="Maximum recommended fat per 100g")
    max_saturated_fat_per_100g: Optional[Decimal] = Field(default=None)
    max_sugars_per_100g: Optional[Decimal] = Field(default=None)
    max_salt_per_100g: Optional[Decimal] = Field(default=None)
    min_fiber_per_100g: Optional[Decimal] = Field(default=None)
    min_protein_per_100g: Optional[Decimal] = Field(default=None)

    # Nutri-score thresholds
    nutri_score_thresholds: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Non-persistent schemas (for validation, forms, API requests/responses)
class FoodItemCreate(SQLModel, table=False):
    """Schema for creating a new food item"""

    name: str = Field(max_length=255)
    brand: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)

    # Nutritional information
    energy_kj: Optional[Decimal] = Field(default=None)
    energy_kcal: Optional[Decimal] = Field(default=None)
    fat: Optional[Decimal] = Field(default=None)
    saturated_fat: Optional[Decimal] = Field(default=None)
    carbohydrates: Optional[Decimal] = Field(default=None)
    sugars: Optional[Decimal] = Field(default=None)
    fiber: Optional[Decimal] = Field(default=None)
    protein: Optional[Decimal] = Field(default=None)
    salt: Optional[Decimal] = Field(default=None)
    sodium: Optional[Decimal] = Field(default=None)

    nutri_score: Optional[NutriScore] = Field(default=None)
    health_assessment: Optional[HealthAssessment] = Field(default=None)

    ingredients: Optional[List[str]] = Field(default=None)
    allergens: Optional[List[str]] = Field(default=None)
    categories: Optional[List[str]] = Field(default=None)


class FoodItemUpdate(SQLModel, table=False):
    """Schema for updating a food item"""

    name: Optional[str] = Field(default=None, max_length=255)
    brand: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)

    # Nutritional information
    energy_kj: Optional[Decimal] = Field(default=None)
    energy_kcal: Optional[Decimal] = Field(default=None)
    fat: Optional[Decimal] = Field(default=None)
    saturated_fat: Optional[Decimal] = Field(default=None)
    carbohydrates: Optional[Decimal] = Field(default=None)
    sugars: Optional[Decimal] = Field(default=None)
    fiber: Optional[Decimal] = Field(default=None)
    protein: Optional[Decimal] = Field(default=None)
    salt: Optional[Decimal] = Field(default=None)
    sodium: Optional[Decimal] = Field(default=None)

    nutri_score: Optional[NutriScore] = Field(default=None)
    health_assessment: Optional[HealthAssessment] = Field(default=None)

    ingredients: Optional[List[str]] = Field(default=None)
    allergens: Optional[List[str]] = Field(default=None)
    categories: Optional[List[str]] = Field(default=None)


class BarcodeCreate(SQLModel, table=False):
    """Schema for creating a new barcode"""

    code: str = Field(max_length=50)
    barcode_type: str = Field(max_length=20)
    food_item_id: int


class ScanResult(SQLModel, table=False):
    """Schema for barcode scan results"""

    barcode: str = Field(description="Scanned barcode")
    found: bool = Field(description="Whether the barcode was found in database")
    food_item: Optional[Dict[str, Any]] = Field(default=None, description="Food item details if found")
    nutri_score: Optional[NutriScore] = Field(default=None)
    health_assessment: Optional[HealthAssessment] = Field(default=None)
    scan_timestamp: datetime = Field(default_factory=datetime.utcnow)


class NutritionSummary(SQLModel, table=False):
    """Schema for nutrition information display"""

    energy_kcal: Optional[Decimal] = Field(default=None)
    fat: Optional[Decimal] = Field(default=None)
    saturated_fat: Optional[Decimal] = Field(default=None)
    carbohydrates: Optional[Decimal] = Field(default=None)
    sugars: Optional[Decimal] = Field(default=None)
    fiber: Optional[Decimal] = Field(default=None)
    protein: Optional[Decimal] = Field(default=None)
    salt: Optional[Decimal] = Field(default=None)


class HealthScore(SQLModel, table=False):
    """Schema for health scoring calculation"""

    nutri_score: NutriScore
    health_assessment: HealthAssessment
    score_factors: Dict[str, Any] = Field(description="Factors contributing to the score")
    recommendations: List[str] = Field(description="Health recommendations")
