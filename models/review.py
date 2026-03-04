from models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy import func

class Review(Base):
    __tablename__ = 'product_review'

    id =mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id = mapped_column(Integer, ForeignKey("product.id", ondelete="CASCADE", onupdate="CASCADE"))

    email = mapped_column(String(30), nullable=False)
    rating = mapped_column(Integer)
    review_content = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="reviews")