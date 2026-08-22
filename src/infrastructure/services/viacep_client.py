import os

import httpx


class ViaCepClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("VIA_CEP") or "https://viacep.com.br/ws/").rstrip("/") + "/"

    def fetch(self, cep: str) -> dict:
        normalized = cep.replace("-", "").replace(" ", "")
        if not normalized.isdigit() or len(normalized) != 8:
            raise ValueError("CEP must contain exactly 8 digits")
        url = f"{self.base_url}{normalized}/json/"
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
        if response.status_code == 400:
            raise ValueError("Invalid CEP format")
        response.raise_for_status()
        return response.json()
