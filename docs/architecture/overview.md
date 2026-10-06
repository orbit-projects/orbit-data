# Orbit Data: architecture and boundaries

## Responsibility

`orbit-data` defines provider-neutral repository and unit-of-work contracts for Orbit applications.
It contains no database driver, SQL dialect, connection pool, or persistence implementation and has
no runtime dependency on Orbit Core.

The package exposes typed `Repository[Entity, Key]` and `UnitOfWork` protocols. `orbit-sql` owns the
provider-neutral SQL contract and implements repositories and unit-of-work behavior on it. Provider
adapters such as `orbit-sql-sqlite`, `orbit-sql-mysql`, and `orbit-sql-postgres` supply connections
without changing repository-facing APIs.

```bash
pip install orbit-data
```

Install `orbit-sql` plus a provider package when an application needs SQL. The SQL capability may
integrate with Core's container lifecycle, but the shared data repository contracts are independent
of Core.

The repository contract provides `get`, bounded `list`, `add`, `update`, and `delete`. Missing reads
return `None`; update/delete report whether they affected a row; writes that violate a uniqueness
constraint raise `RepositoryConflictError`, without exposing driver messages or stored values. A
unit of work is an async context that commits on normal exit and rolls back on exceptions or
cancellation. Repositories obtained from it must not outlive that context.

The contracts intentionally do not prescribe object-relational mapping, schema migrations, identity
generation, query filtering, or repository discovery. Implementations must document those choices.

## Declared dependencies

The following dependency declarations come from the checked-in manifests. Optional groups and development dependencies are called out separately.

### `pyproject.toml`
- No dependencies declared.
- Optional `dev` group: `pytest>=8,<10`, `ruff>=0.8,<1`, `mypy>=1.13,<2`.

Declared dependencies do not mean that optional providers or services are bundled with this package.

## Implementation layout

Representative implementation files in this checkout:

- `src/orbit_data/__init__.py`
- `src/orbit_data/contracts.py`
- `src/orbit_data/errors.py`

## Public contract and scope

## Status

This package is pre-alpha; its API is not stable and it is not yet a published release. It supports
Python 3.11 through 3.14.

## Boundary rules

Keep provider SDKs, credentials, transports, and provider-specific error translation in provider adapters. Keep reusable capability contracts in the matching capability package and lifecycle orchestration in Core. Apply the relevant layer for this repository and preserve the dependency direction shown above.
