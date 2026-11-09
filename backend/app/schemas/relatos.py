"""Contratos validados entre cidadão, API e provedor de IA."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

Categoria = Literal[
    "Vias e buracos", "Calçadas e acessibilidade", "Iluminação pública",
    "Lixo e limpeza", "Drenagem e alagamentos", "Outros",
]
Prioridade = Literal["alta", "media", "baixa"]

CATEGORIAS = list(Categoria.__args__)
PRIORIDADES = ["alta", "media", "baixa"]


class RelatoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    bairro: str = Field(min_length=3, max_length=60)
    categoria_informada: Categoria
    descricao: str = Field(min_length=30, max_length=900)

    @field_validator("bairro", "descricao")
    @classmethod
    def apenas_texto_legivel(cls, value: str) -> str:
        if any(ord(c) < 32 and c not in "\n\t" for c in value):
            raise ValueError("Texto contém caracteres não permitidos")
        return value


class ResultadoIA(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    categoria: Categoria
    prioridade: Prioridade
    resumo: str = Field(min_length=12, max_length=220)
    justificativa: str = Field(min_length=12, max_length=260)
    orientacao: str = Field(min_length=25, max_length=400)
    encaminhamento: str = Field(min_length=8, max_length=120)
    atencao_imediata: bool


class RespostaAnalise(BaseModel):
    resultado: ResultadoIA
    modo: Literal["llm", "demonstracao"]
    aviso: str


class SaudeResposta(BaseModel):
    status: Literal["ok"] = "ok"
    modo: Literal["llm", "demonstracao"]
