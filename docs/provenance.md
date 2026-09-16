# Publisher Provenance

## Purpose

This repository uses a low-salience origin ID plus an Ed25519 publisher signature. The origin ID is a non-executable watermark; it does not transmit data, grant access, bypass permissions, or identify an installer. The signature is the actual authorship evidence.

Official origin ID:

```text
5066c921-6f07-4768-9fe1-412f9931adca
```

Prepared publisher-key SHA-256 fingerprint:

```text
d64d7ebc963fdaa86a44573bd226e8bb135d9d95818c5f39df88e0a45e886596
```

Official repository:

```text
https://github.com/PDBen-Auto/amazon-product-decision-suite
```

## Evidence Chain

1. `PUBLIC_MANIFEST.sha256` binds the prepared public files.
2. `RELEASE_PROVENANCE.json` binds the manifest hash, Skill name, version, origin ID, timestamp, and publisher-key fingerprint.
3. `RELEASE_PROVENANCE.sig` is an Ed25519 signature over the canonical provenance JSON.
4. `PUBLISHER_PUBLIC_KEY.pem` verifies the signature.
5. The public-key SHA-256 fingerprint must also be published through an independent trusted channel such as the publisher's GitHub profile, a signed Git tag, a personal domain, or a timestamped transparency service.

A public key stored only inside the same repository is not sufficient identity proof because a copier can replace the key and resign a modified package. The independent fingerprint anchor is what connects the cryptographic key to the publisher.

## Release Verification

```bash
python scripts/build_release_manifest.py . --check
python scripts/release_provenance.py verify-release \
  --manifest PUBLIC_MANIFEST.sha256 \
  --provenance RELEASE_PROVENANCE.json \
  --signature RELEASE_PROVENANCE.sig \
  --public-key PUBLISHER_PUBLIC_KEY.pem \
  --expected-origin-id 5066c921-6f07-4768-9fe1-412f9931adca \
  --expected-fingerprint d64d7ebc963fdaa86a44573bd226e8bb135d9d95818c5f39df88e0a45e886596
```

## Publishing a New Version

1. Make reviewed source changes.
2. Run all tests and the public-boundary scan.
3. Regenerate `PUBLIC_MANIFEST.sha256`.
4. Sign the manifest with the offline publisher private key.
5. Verify the release using the externally anchored fingerprint.
6. Commit the manifest, provenance JSON, signature, and public key.
7. Create a protected, signed Git tag and GitHub Release.

Never commit the publisher private key or its passphrase. Keep at least one encrypted offline backup. If the key is exposed, publish a signed revocation notice where possible, rotate the key, and update every trusted fingerprint channel.

## Dispute Challenge

When authorship is disputed, a neutral party supplies a new random challenge. The publisher signs that exact text:

```bash
python scripts/release_provenance.py sign-challenge \
  --challenge "<random-challenge>" \
  --origin-id 5066c921-6f07-4768-9fe1-412f9931adca \
  --private-key <offline-private-key.pem> \
  --output challenge-response.json
```

The neutral party verifies it with `verify-challenge`. This proves current possession of the same private key without revealing the key.

## Watermark Limitations

The origin ID appears in more than one low-profile location to survive ordinary copying. It is not secret and can be removed or copied by a determined editor. Do not use it alone as proof of authorship. Do not add invisible Unicode, secret network calls, undisclosed telemetry, authentication bypasses, or remote-control behavior as a watermark.
