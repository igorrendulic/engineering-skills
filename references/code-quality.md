# Code Quality

Choose the simplest understandable solution that satisfies current requirements
and preserves required correctness, safety, and compatibility. Simplicity takes
precedence over speculative future extensibility. Add abstractions, configuration,
dependencies, and extension points only when the current task needs them; future
expansion can be addressed in subsequent work.

Apply the following concerns in proportion to the affected behavior and its
consequences. In planning, turn applicable material concerns into acceptance
criteria and verification. During implementation, apply them to the code and
actual results, including when there is no separate plan. Do not invent new
requirements, add machinery, or create reporting artifacts merely to cover every
row.

| Concern | Guidance |
| --- | --- |
| Correctness | Define expected behavior, important boundaries and failure cases, and invariants that must remain true. |
| Usability | Make the affected user or caller workflow usable through its normal entry point, with understandable inputs, outputs, and errors. Include accessibility when relevant. |
| Readability | Use clear domain names, direct control flow, and cohesive responsibilities. Make state changes and side effects apparent; explain non-obvious reasons when needed. |
| Maintainability | Fit existing ownership and contracts. Keep changes localized and reuse code when behavior matches. Avoid layers or generalization intended only for possible future use. |
| Reliability and data integrity | Address relevant partial failures, retries, concurrency, and recovery without speculative defensive machinery. |
| Security and privacy | Preserve affected trust and authorization boundaries; handle untrusted input, secrets, and sensitive data appropriately. |
| Performance | Consider the actual workload and resource bounds. Measure material concerns before adding optimization complexity. |
| Operability | Make relevant failures diagnosable using existing mechanisms. Update affected usage or configuration guidance when needed for consumers. |

Use evidence appropriate to each claim: behavioral tests, representative runtime
checks, measurements, or direct code inspection. Passing tests alone does not
establish readability or usability. Reuse sufficient evidence and identify material
gaps rather than treating unperformed checks as proof.
