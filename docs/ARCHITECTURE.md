# Architecture

## Trust Boundaries

```text
[User-controlled evidence]
          |
          v
[Public Gateway]
  validation, minimization, authorization, hashing
          |
          | HTTPS / scoped token
          v
[Private Engine]
  proprietary orchestration and decision methods
          |
          | signed response
          v
[Public Gateway]
  schema, request hash, result hash, signature verification
```

The public repository never needs the Engine source or signing private key. The Engine never needs repository write access.

## Request Lifecycle

1. Freeze marketplace, currency, as-of date, target product, concept version, decision question, and requested outputs.
2. Remove credentials, cookies, personal data, confidential supplier contacts, internal paths, and presigned URLs.
3. Validate the request contract locally.
4. Show the destination and transmitted data categories to the user.
5. Submit one authorized HTTPS request with a short-lived token.
6. Require the response to bind the exact request SHA-256.
7. Verify the response payload hash and Ed25519 signature.
8. Present the Engine result without adding hidden local scoring.

## Release Provenance

Repository provenance and Engine-result provenance use separate keys. The publisher key signs the public release manifest; the Engine key signs decision responses; Git commit or tag signing should use a third identity key where practical.

## Threat Model

The design reduces accidental source disclosure, credential leakage, response forgery, token leakage through redirects, and modified-copy impersonation. It cannot prevent someone from changing a local public clone. Official identity depends on the trusted repository, signed release, and separately anchored publisher fingerprint.
