
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re

class EmpresaOut(BaseModel):
    id: int
    nome_empresa: str
    nicho: str
    telefone: str | None = None
    email_login: EmailStr
    tipo_empresa: str | None = None
    plano_empresa: str | None = None
    limite_clientes: int | None = None
    limite_atendimentos: int | None = None
    ativo: int | None = None
    model_config = {
        "from_attributes": True
    }

class EmpresaLogin(BaseModel):
    email_login: EmailStr
    senha: str
    model_config = {
        "from_attributes": True
    }


class RefreshRequest(BaseModel):
    refresh_token: str
    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    model_config = {
        "from_attributes": True
    }


class EmpresaCreate(BaseModel):
    nome_empresa: str = Field(min_length=3, max_length=255, description="Nome da empresa")
    nicho: str = Field(min_length=3, max_length=100, description="Nicho de atuação")
    telefone: str | None = Field(None, pattern=r"^\+?[\d\s\-\(\)]{10,}$", description="Telefone com DDD")
    email_login: EmailStr = Field(description="Email para login")
    senha: str = Field(min_length=8, description="Senha com mínimo 8 caracteres")
    tipo_empresa: str | None = None
    plano_empresa: str | None = None
    limite_clientes: int | None = None
    limite_atendimentos: int | None = None
    
    @field_validator('senha')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Valida força da senha"""
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve conter pelo menos um número')
        if not any(c.isalpha() for c in v):
            raise ValueError('Senha deve conter pelo menos uma letra')
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        return v
    
    @field_validator('nome_empresa')
    @classmethod
    def validate_nome_empresa(cls, v: str) -> str:
        """Valida nome da empresa"""
        if not v or not v.strip():
            raise ValueError('Nome da empresa não pode estar vazio')
        return v.strip()
    
    model_config = {
        "from_attributes": True
    }

class ClienteCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=255, description="Nome do cliente")
    telefone: str = Field(pattern=r"^\+?[\d\s\-\(\)]{10,}$", description="Telefone com DDD")
    anotacoes_rapidas: str = Field(default="", max_length=1000)
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v: str) -> str:
        """Valida nome do cliente"""
        if not v or not v.strip():
            raise ValueError('Nome do cliente não pode estar vazio')
        return v.strip()
    
    @field_validator('telefone')
    @classmethod
    def validate_telefone(cls, v: str) -> str:
        """Remove formatação e valida telefone"""
        # Remove espaços e caracteres especiais para validação
        digits = re.sub(r'[^\d]', '', v)
        if len(digits) < 10:
            raise ValueError('Telefone deve conter pelo menos 10 dígitos')
        if len(digits) > 15:
            raise ValueError('Telefone não pode ter mais de 15 dígitos')
        return v
    
    model_config = {
        "from_attributes": True
    }

class AtendimentoCreate(BaseModel):
    tipo: str = Field(min_length=2, max_length=100, description="Tipo de atendimento")
    descricao: str = Field(min_length=5, max_length=2000, description="Descrição do atendimento")
    veiculo: str = Field(max_length=255, description="Informações do veículo")
    
    @field_validator('tipo', 'descricao', 'veiculo')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Valida que campos não estão vazios"""
        if not v or not v.strip():
            raise ValueError('Campo não pode estar vazio')
        return v.strip()
    
    model_config = {
        "from_attributes": True
    }

class ClienteOut(BaseModel):
    id: int
    nome: str
    telefone: str
    anotacoes_rapidas: str = ""
    data_primeiro_contato: datetime
    model_config = {
        "from_attributes": True
    }

class PerguntaIA(BaseModel):
    pergunta: str = Field(min_length=3, max_length=1000, description="Pergunta para a IA")
    
    @field_validator('pergunta')
    @classmethod
    def validate_pergunta(cls, v: str) -> str:
        """Valida e sanitiza pergunta"""
        if not v or not v.strip():
            raise ValueError('Pergunta não pode estar vazia')
        # Limita caracteres especiais consecutivos para prevenir injection
        v = re.sub(r'([^\w\s])\1{3,}', r'\1\1', v)
        return v.strip()
    
    model_config = {
        "from_attributes": True
    }
