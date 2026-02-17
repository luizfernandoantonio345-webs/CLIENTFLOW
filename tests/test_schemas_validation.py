"""
Testes para validação de schemas do ClientFlow
"""
import pytest
from pydantic import ValidationError
from backend.schemas import (
    EmpresaCreate,
    ClienteCreate,
    AtendimentoCreate,
    PerguntaIA,
    EmpresaLogin
)


class TestEmpresaCreateValidation:
    """Testes de validação para criação de empresa"""
    
    def test_empresa_create_valida(self):
        """Testa criação de empresa com dados válidos"""
        empresa = EmpresaCreate(
            nome_empresa="Oficina do João",
            nicho="Mecânica",
            telefone="(11) 98765-4321",
            email_login="joao@oficina.com",
            senha="Senha123"
        )
        assert empresa.nome_empresa == "Oficina do João"
        assert empresa.email_login == "joao@oficina.com"
    
    def test_senha_minimo_8_caracteres(self):
        """Testa que senha deve ter mínimo 8 caracteres"""
        with pytest.raises(ValidationError) as exc_info:
            EmpresaCreate(
                nome_empresa="Oficina",
                nicho="Mecânica",
                email_login="test@test.com",
                senha="abc123"  # Apenas 6 caracteres
            )
        assert "8 characters" in str(exc_info.value).lower()
    
    def test_senha_deve_conter_numero(self):
        """Testa que senha deve conter pelo menos um número"""
        with pytest.raises(ValidationError) as exc_info:
            EmpresaCreate(
                nome_empresa="Oficina",
                nicho="Mecânica",
                email_login="test@test.com",
                senha="SenhaForte"  # Sem números
            )
        assert "número" in str(exc_info.value).lower()
    
    def test_senha_deve_conter_letra(self):
        """Testa que senha deve conter pelo menos uma letra"""
        with pytest.raises(ValidationError) as exc_info:
            EmpresaCreate(
                nome_empresa="Oficina",
                nicho="Mecânica",
                email_login="test@test.com",
                senha="12345678"  # Sem letras
            )
        assert "letra" in str(exc_info.value).lower()
    
    def test_email_invalido(self):
        """Testa que email deve ser válido"""
        with pytest.raises(ValidationError):
            EmpresaCreate(
                nome_empresa="Oficina",
                nicho="Mecânica",
                email_login="email_invalido",  # Email sem @
                senha="Senha123"
            )
    
    def test_nome_empresa_minimo_3_caracteres(self):
        """Testa que nome da empresa deve ter mínimo 3 caracteres"""
        with pytest.raises(ValidationError):
            EmpresaCreate(
                nome_empresa="AB",  # Apenas 2 caracteres
                nicho="Mecânica",
                email_login="test@test.com",
                senha="Senha123"
            )
    
    def test_nome_empresa_nao_vazio(self):
        """Testa que nome da empresa não pode estar vazio"""
        with pytest.raises(ValidationError):
            EmpresaCreate(
                nome_empresa="   ",  # Apenas espaços
                nicho="Mecânica",
                email_login="test@test.com",
                senha="Senha123"
            )
    
    def test_telefone_formato_valido(self):
        """Testa diferentes formatos válidos de telefone"""
        formatos_validos = [
            "(11) 98765-4321",
            "11987654321",
            "+55 11 98765-4321",
            "11 9 8765-4321"
        ]
        for telefone in formatos_validos:
            empresa = EmpresaCreate(
                nome_empresa="Oficina",
                nicho="Mecânica",
                telefone=telefone,
                email_login="test@test.com",
                senha="Senha123"
            )
            assert empresa.telefone == telefone


class TestClienteCreateValidation:
    """Testes de validação para criação de cliente"""
    
    def test_cliente_create_valido(self):
        """Testa criação de cliente com dados válidos"""
        cliente = ClienteCreate(
            nome="João Silva",
            telefone="(11) 98765-4321",
            anotacoes_rapidas="Cliente preferencial"
        )
        assert cliente.nome == "João Silva"
        assert cliente.telefone == "(11) 98765-4321"
    
    def test_nome_minimo_2_caracteres(self):
        """Testa que nome deve ter mínimo 2 caracteres"""
        with pytest.raises(ValidationError):
            ClienteCreate(
                nome="A",  # Apenas 1 caractere
                telefone="11987654321"
            )
    
    def test_nome_nao_vazio(self):
        """Testa que nome não pode estar vazio"""
        with pytest.raises(ValidationError):
            ClienteCreate(
                nome="   ",  # Apenas espaços
                telefone="11987654321"
            )
    
    def test_telefone_minimo_10_digitos(self):
        """Testa que telefone deve ter pelo menos 10 dígitos"""
        with pytest.raises(ValidationError) as exc_info:
            ClienteCreate(
                nome="João Silva",
                telefone="123456789"  # Apenas 9 dígitos
            )
        # Pode falhar por pattern ou por validação customizada
        assert ("pattern" in str(exc_info.value).lower() or 
                "10 dígitos" in str(exc_info.value).lower())
    
    def test_telefone_maximo_15_digitos(self):
        """Testa que telefone não pode ter mais de 15 dígitos"""
        with pytest.raises(ValidationError) as exc_info:
            ClienteCreate(
                nome="João Silva",
                telefone="1234567890123456"  # 16 dígitos
            )
        assert "15 dígitos" in str(exc_info.value).lower()
    
    def test_telefone_formatos_validos(self):
        """Testa diferentes formatos válidos de telefone"""
        formatos = [
            "(11) 98765-4321",
            "11987654321",
            "+55 11 98765-4321",
            "11 9 8765-4321"
        ]
        for telefone in formatos:
            cliente = ClienteCreate(
                nome="João Silva",
                telefone=telefone
            )
            assert cliente.telefone == telefone


class TestAtendimentoCreateValidation:
    """Testes de validação para criação de atendimento"""
    
    def test_atendimento_create_valido(self):
        """Testa criação de atendimento com dados válidos"""
        atendimento = AtendimentoCreate(
            tipo="Manutenção",
            descricao="Troca de óleo e filtros",
            veiculo="Fiat Uno 2015"
        )
        assert atendimento.tipo == "Manutenção"
        assert atendimento.descricao == "Troca de óleo e filtros"
    
    def test_tipo_minimo_2_caracteres(self):
        """Testa que tipo deve ter mínimo 2 caracteres"""
        with pytest.raises(ValidationError):
            AtendimentoCreate(
                tipo="M",  # Apenas 1 caractere
                descricao="Troca de óleo",
                veiculo="Fiat Uno"
            )
    
    def test_descricao_minimo_5_caracteres(self):
        """Testa que descrição deve ter mínimo 5 caracteres"""
        with pytest.raises(ValidationError):
            AtendimentoCreate(
                tipo="Manutenção",
                descricao="Test",  # Apenas 4 caracteres
                veiculo="Fiat Uno"
            )
    
    def test_campos_nao_vazios(self):
        """Testa que campos não podem estar vazios"""
        with pytest.raises(ValidationError):
            AtendimentoCreate(
                tipo="   ",  # Apenas espaços
                descricao="Descrição válida",
                veiculo="Fiat Uno"
            )


class TestPerguntaIAValidation:
    """Testes de validação para perguntas à IA"""
    
    def test_pergunta_valida(self):
        """Testa pergunta válida"""
        pergunta = PerguntaIA(
            pergunta="Quantos clientes eu tenho?"
        )
        assert pergunta.pergunta == "Quantos clientes eu tenho?"
    
    def test_pergunta_minimo_3_caracteres(self):
        """Testa que pergunta deve ter mínimo 3 caracteres"""
        with pytest.raises(ValidationError):
            PerguntaIA(pergunta="AB")  # Apenas 2 caracteres
    
    def test_pergunta_nao_vazia(self):
        """Testa que pergunta não pode estar vazia"""
        with pytest.raises(ValidationError):
            PerguntaIA(pergunta="   ")  # Apenas espaços
    
    def test_pergunta_sanitizada(self):
        """Testa que caracteres especiais consecutivos são limitados"""
        pergunta = PerguntaIA(
            pergunta="Quantos!!!!! clientes?????"
        )
        # Deve limitar caracteres especiais consecutivos
        assert "!!!!!" not in pergunta.pergunta or "?????" not in pergunta.pergunta


class TestEmpresaLoginValidation:
    """Testes de validação para login de empresa"""
    
    def test_login_valido(self):
        """Testa login com dados válidos"""
        login = EmpresaLogin(
            email_login="teste@teste.com",
            senha="Senha123"
        )
        assert login.email_login == "teste@teste.com"
    
    def test_email_invalido_no_login(self):
        """Testa que email deve ser válido no login"""
        with pytest.raises(ValidationError):
            EmpresaLogin(
                email_login="email_invalido",  # Sem @
                senha="Senha123"
            )
