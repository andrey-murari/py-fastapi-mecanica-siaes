import os
from typing import override

import httpx

from src.ports.driving.for_get_address.for_get_address import ForGetAddress
from src.ports.driver.for_manage_relationship.dto import AddressDTO


class ViacepAdapter(ForGetAddress):
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (
            base_url
            or os.getenv("VIA_CEP_BASE_URL")
            or os.getenv("VIA_CEP")
            or "https://viacep.com.br/ws/"
        ).rstrip("/") + "/"

    @override
    def get_address_by_cep(self, cep: str) -> AddressDTO:
        normalized = cep.replace("-", "").replace(" ", "")
        if not normalized.isdigit() or len(normalized) != 8:
            raise ValueError("CEP must contain exactly 8 digits")
        url = f"{self.base_url}{normalized}/json/"
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
        if response.status_code == 400:
            raise ValueError("Invalid CEP format")
        response.raise_for_status()
        if response.json().get("erro") in (True, "true"):
            raise ValueError("CEP not found on ViaCEP")
        return AddressDTO(
            cep_id=str(response.json().get("cep", "")),
            street=response.json().get("logradouro") or "",
            neighborhood=response.json().get("bairro") or "",
            city=response.json().get("localidade") or "",
            state=response.json().get("uf") or "",
        )


viacep_adapter = ViacepAdapter()