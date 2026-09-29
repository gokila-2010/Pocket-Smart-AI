from sqlalchemy import Column, Integer, String, Text
from database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)

    category = Column(String, nullable=False)

    input_details = Column(Text, nullable=False)

    recommendation = Column(Text, nullable=False)