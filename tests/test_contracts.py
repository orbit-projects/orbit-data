# Copyright 2026-present Orbit Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Structural checks for the public repository and unit-of-work protocols."""

from __future__ import annotations

from types import TracebackType

from orbit_data import Repository, UnitOfWork


class MemoryRepository:
    """Small protocol fixture with deterministic CRUD semantics."""

    async def get(self, key: int) -> str | None:
        return str(key) if key == 1 else None

    async def list(self, *, limit: int = 100) -> tuple[str, ...]:
        return ("one",)[:limit]

    async def add(self, entity: str) -> None:
        return None

    async def update(self, entity: str) -> bool:
        return entity == "one"

    async def delete(self, key: int) -> bool:
        return key == 1


class MemoryUnitOfWork:
    """Protocol fixture that is safe to use as an async context manager."""

    async def __aenter__(self) -> MemoryUnitOfWork:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        return False


def test_repository_and_unit_of_work_are_structural_protocols() -> None:
    assert isinstance(MemoryRepository(), Repository)
    assert isinstance(MemoryUnitOfWork(), UnitOfWork)
