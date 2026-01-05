from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column, Integer, String, Date, Numeric, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.storage import note_storage


class Note(Base):
	__tablename__ = "notes"

	id = Column(Integer, primary_key=True, index=True)
	note_type = Column(String(50), nullable=False)
	note_number = Column(String(100), nullable=True)
	series = Column(String(50), nullable=True)
	access_key = Column(String(100), nullable=True)
	issuer_cnpj = Column(String(20), nullable=True)
	issuer_ie = Column(String(20), nullable=True)
	issuer_city = Column(String(100), nullable=True)
	issuer_state = Column(String(2), nullable=True)
	issuer_zip_code = Column(String(10), nullable=True)
	provider = Column(String(255), nullable=False)
	nature_of_operation = Column(String(255), nullable=True)
	protocol_number = Column(String(100), nullable=True)
	date_of_issue = Column(Date, nullable=False)
	total_value = Column(Numeric(12, 2), nullable=False)
	pdf_url = Column(Text, nullable=False)
	pdf_file = Column(FileType(storage=note_storage))
	created_at = Column(DateTime(timezone=True), server_default=func.now())

	items = relationship("ItemNote", back_populates="note", cascade="all, delete-orphan")

	def __str__(self) -> str:
		return f"Nota {self.note_number} - {self.provider}"


class ItemNote(Base):
	__tablename__ = "note_items"

	id = Column(Integer, primary_key=True, index=True)
	note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
	product_name = Column(String(255), nullable=False)
	product_code = Column(String(100), nullable=True)
	ncm = Column(String(20), nullable=True)
	cfop = Column(String(10), nullable=True)
	discount_value = Column(Numeric(12, 4), nullable=True)
	icms_value = Column(Numeric(12, 4), nullable=True)
	ipi_value = Column(Numeric(12, 4), nullable=True)
	quantity = Column(Numeric(14, 4), nullable=True)
	unit_of_measure = Column(String(10), nullable=True)
	unit_value = Column(Numeric(12, 4), nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())

	note = relationship("Note", back_populates="items")

	def __str__(self) -> str:
		return self.product_name
