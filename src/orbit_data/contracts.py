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
"""Provider-neutral repository and transaction-scope contracts for Orbit data packages."""

from __future__ import annotations

from types import TracebackType
from typing import Protocol, TypeVar, runtime_checkable

EntityT = TypeVar("EntityT")
KeyT = TypeVar("KeyT", contravariant=True)


@runtime_checkable
class Repository(Protocol[EntityT, KeyT]):
    """Typed CRUD boundary for one entity type and its application-defined key type.

    Implementations return ``None`` from ``get`` when a key is absent. ``update`` and ``delete``
    return whether an existing record was affected. Writes that violate a uniqueness constraint
    raise :class:`orbit_data.RepositoryConflictError` without exposing provider details.
    """

    async def get(self, key: KeyT) -> EntityT | None:
        """Return one entity by key, or ``None`` when it does not exist."""

    async def list(self, *, limit: int = 100) -> tuple[EntityT, ...]:
        """Return a stable, bounded page of entities."""

    async def add(self, entity: EntityT) -> None:
        """Insert an entity without mutating the supplied object."""

    async def update(self, entity: EntityT) -> bool:
        """Replace the stored entity with the same key; return whether it existed."""

    async def delete(self, key: KeyT) -> bool:
        """Delete an entity by key and report whether one was present."""


@runtime_checkable
class UnitOfWork(Protocol):
    """Async transaction scope that commits on normal exit and rolls back on failure.

    Implementations must include cancellation in the failure path and release all owned resources
    before leaving the context. Repository objects obtained from a unit of work must not outlive it.
    """

    async def __aenter__(self) -> UnitOfWork:
        """Begin the transaction and return its unit-of-work facade."""

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Commit on success or roll back on any exception, including cancellation."""


__all__ = ["Repository", "UnitOfWork"]
