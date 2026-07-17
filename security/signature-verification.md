# Signature Verification

## Current status

PersistMind `0.2.1.dev15` is unsigned. There is no valid signature-verification
step that can promote it into the trusted updater channel.

## Future signed releases

A signed release must verify:

- the configured trusted public key;
- the signature over the canonical manifest bytes;
- product, channel, version, source commit, and expiry;
- exact artifact filename, byte size, and SHA-256; and
- installed package identity after installation.

Signature failure must stop installation. Never copy, request, log, publish, or
bundle the private signing key. Never replace signature verification with a
checksum-only check for a channel that requires authentication.
