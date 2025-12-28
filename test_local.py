import json
from src.lambda_handler import lambda_handler


def test_authentication():
    """Teste de autenticação com CPF válido."""
    print("=" * 60)
    print("TESTE: Autenticação com CPF válido")
    print("=" * 60)
    
    event = {
        "body": json.dumps({
            "cpf": "11144477735"
        })
    }
    
    response = lambda_handler(event, None)
    print(f"\nStatus Code: {response['statusCode']}")
    print(f"Response Body: {response['body']}")
    print()


def test_invalid_cpf():
    """Teste com CPF inválido."""
    print("=" * 60)
    print("TESTE: CPF inválido")
    print("=" * 60)
    
    event = {
        "body": json.dumps({
            "cpf": "00000000000"
        })
    }
    
    response = lambda_handler(event, None)
    print(f"\nStatus Code: {response['statusCode']}")
    print(f"Response Body: {response['body']}")
    print()


def test_customer_not_found():
    """Teste com CPF não cadastrado."""
    print("=" * 60)
    print("TESTE: Cliente não encontrado")
    print("=" * 60)
    
    event = {
        "body": json.dumps({
            "cpf": "76974694059"
        })
    }
    
    response = lambda_handler(event, None)
    print(f"\nStatus Code: {response['statusCode']}")
    print(f"Response Body: {response['body']}")
    print()


def test_missing_cpf():
    """Teste sem CPF no body."""
    print("=" * 60)
    print("TESTE: CPF ausente")
    print("=" * 60)
    
    event = {
        "body": json.dumps({})
    }
    
    response = lambda_handler(event, None)
    print(f"\nStatus Code: {response['statusCode']}")
    print(f"Response Body: {response['body']}")
    print()


if __name__ == "__main__":
    from dotenv import load_dotenv
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    print("\n🚀 TESTES DA API DE AUTENTICAÇÃO\n")
    
    try:
        test_authentication()
        test_invalid_cpf()
        test_customer_not_found()
        test_missing_cpf()
        
        print("=" * 60)
        print("✅ Todos os testes foram executados!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
