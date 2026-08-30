from datetime import datetime

from src.domain.relationship.entities import Address
from src.domain.relationship.entities import Person


def stub_viacep_payload() -> dict:
    return {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "complemento": "lado ímpar",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
        "estado": "São Paulo",
        "regiao": "Sudeste",
        "ibge": "3550308",
        "gia": "1004",
        "ddd": "11",
        "siafi": "7107",
    }


def stub_address():
    return Address(
        cep_id="01001000",
        street="Praça da Sé",
        neighborhood="Sé",
        city="São Paulo",
        state="SP",
        user_modification_id=1,
        flag_active=True,
        insertion_date=datetime.now(),
        modification_date=datetime.now(),
    )


def stub_person():
    return Person(
        person_id="52998224725",
        complete_name="Andrey Murari",
        user_id="52998224725",
        user_modification_id=1,
        flag_active=True,
        insertion_date=datetime.now(),
        modification_date=datetime.now(),
    )


