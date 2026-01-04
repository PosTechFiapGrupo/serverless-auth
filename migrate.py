import uuid
from sqlalchemy import create_engine
from src.infrastructure.database.models import Base
from src.infrastructure.config.settings import get_settings


def create_tables():
    """Create all database tables."""
    settings = get_settings()
    engine = create_engine(settings.database_url)

    # Create tables
    Base.metadata.create_all(engine)
    print("✓ Tables created successfully!")


def create_sample_data():
    """Create sample customer data for testing."""
    from sqlalchemy.orm import sessionmaker
    from src.infrastructure.database.models import CustomerModel
    from datetime import datetime

    settings = get_settings()
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check if data already exists
        existing = session.query(CustomerModel).first()
        if existing:
            print("Sample data already exists. Skipping...")
            return

        # Create sample customers with production schema
        customers = [
            CustomerModel(
                id=str(uuid.uuid4()),
                cpf="111.444.777-35",
                nome="João da Silva",
                telefone="11987654321",
                email="joao@example.com",
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow(),
            ),
            CustomerModel(
                id=str(uuid.uuid4()),
                cpf="529.982.247-25",
                nome="Maria Santos",
                telefone="11912345678",
                email="maria@example.com",
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow(),
            ),
            CustomerModel(
                id=str(uuid.uuid4()),
                cpf="390.533.447-05",
                nome="Pedro Oliveira",
                telefone="11998765432",
                email="pedro@example.com",
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow(),
            ),
        ]

        session.add_all(customers)
        session.commit()
        print("✓ Sample data created successfully!")
        print("\nSample CPFs for testing:")
        for customer in customers:
            cpf_digits = "".join(filter(str.isdigit, customer.cpf))
            print(f"  - {customer.cpf} ({cpf_digits}) - {customer.nome}")

    except Exception as e:
        session.rollback()
        print(f"✗ Error creating sample data: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    print("Database Migration Script")
    print("=" * 50)

    if len(sys.argv) > 1 and sys.argv[1] == "--with-sample-data":
        print("\n1. Creating tables...")
        create_tables()
        print("\n2. Creating sample data...")
        create_sample_data()
    else:
        print("\nCreating tables...")
        create_tables()
        print("\nTo create sample data, run: python migrate.py --with-sample-data")
