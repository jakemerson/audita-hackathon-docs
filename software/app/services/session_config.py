"""Configuração efêmera da sessão do processo; nunca persiste nem revela a chave."""

from __future__ import annotations

from threading import RLock

from app.services.openai_auditor import usable_key


class SessionKeyStore:
    def __init__(self) -> None:
        self._key: str | None = None
        self._lock = RLock()

    def set(self, value: str | None) -> bool:
        with self._lock:
            self._key = value.strip() if usable_key(value) else None
            return self._key is not None

    def get(self) -> str | None:
        with self._lock:
            return self._key

    @property
    def configured(self) -> bool:
        with self._lock:
            return self._key is not None


key_store = SessionKeyStore()
