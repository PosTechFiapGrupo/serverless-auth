from typing import Optional
from sqlalchemy.orm import Session

from src.domain.entities import Customer
from src.application.use_cases.ports import ICustomerRepository
from src.infrastructure.database.models import CustomerModel


class CustomerRepository(ICustomerRepository):
    """
    Customer Repository implementation.
    
    Adapter between domain layer and database infrastructure.
    Uses SQLAlchemy ORM for data access.
    """
    
    def __init__(self, session: Session):
        self._session = session
    
    def find_by_cpf(self, cpf: str) -> Optional[Customer]:
        """
        Find customer by CPF.
        
        Args:
            cpf: Clean CPF number (only digits)
            
        Returns:
            Customer entity or None if not found
        """
        try:
            cpf_digits = ''.join(filter(str.isdigit, cpf))
            
            all_customers = self._session.query(CustomerModel).all()
            
            for customer_model in all_customers:
                if customer_model.cpf:
                    db_cpf_clean = ''.join(filter(str.isdigit, customer_model.cpf))
                    if db_cpf_clean == cpf_digits:
                        return self._to_entity(customer_model)
            
            return None
            
        except Exception:
            return None
    
    @staticmethod
    def _to_entity(model: CustomerModel) -> Customer:
        """Convert database model to domain entity."""
        cpf_clean = ''.join(filter(str.isdigit, model.cpf)) if model.cpf else ''
        
        return Customer(
            id=model.id,
            cpf=cpf_clean,
            nome=model.nome,
            email=model.email,
            telefone=model.telefone,
            criado_em=model.criado_em,
            atualizado_em=model.atualizado_em
        )
