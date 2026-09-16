# Private Engine Deployment

The public Gateway becomes operational only after a separate private service is deployed.

## Required Controls

- HTTPS endpoint with no token-bearing redirects
- Short-lived, scoped authentication tokens
- Request-size limits, rate limits, quotas, and audit logs
- Tenant isolation and data minimization
- Documented retention and deletion policy
- Engine version recorded in every response
- Ed25519 result-signing key held in a managed secret or key service
- Monitoring for threshold probing and method-extraction attempts
- Revocation and key-rotation procedure

## Required Configuration

```text
AMAZON_DECISION_API_URL
AMAZON_DECISION_API_TOKEN
AMAZON_DECISION_PUBLIC_KEY
```

The public repository must never contain the service token, result-signing private key, production request bodies, supplier records, or private Engine source.

## Failure Behavior

- Authentication, validation, and authorization failures are not retried automatically.
- A single retry is allowed only for an obvious transient network timeout when duplicate processing is impossible.
- Unsigned, hash-mismatched, or unverifiable results cannot support purchasing or launch approval.
- When the service is unavailable, preserve the validated request and report `ENGINE_UNAVAILABLE`; do not invent a local verdict.
