# Orbit Data: operations and security

This guide organizes runtime behavior documented by the package. It does not certify production readiness. Verify provider/client versions, permissions, transport security, limits, and failure behavior in the target environment before release.

## Configuration surface

Environment names found in the package README:

The package README does not name `ORBIT_*` variables. Use its typed constructors and application configuration, and confirm exact runtime inputs in the implementation before deployment.

Use the package README's constructor and deployment examples. Store credentials in a secret manager and avoid logging credentials, raw provider errors, request data, or opaque cursors.

## Lifecycle, failure behavior, and limits

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

## Status

This package is pre-alpha; its API is not stable and it is not yet a published release. It supports
Python 3.11 through 3.14.

## Production validation

Validate startup/shutdown cleanup, timeout and cancellation behavior, concurrency and payload bounds where applicable, secret rotation and least-privilege access, data durability, backup/restore, and failover against the selected provider. Do not infer distributed or durable guarantees from an in-process API or fake-client tests.
