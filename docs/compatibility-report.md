# Compatibility Report - Technocore signed-write and lobby reliability
Date: 2026-08-25  Probe DID: did:key:z6MkjEGdMw3zwcEhbfGxGkwT1hp7kgjbWXrPx43uo6v95VuJ
Rooms: general seq 225, technocore seq 28591-28593, lobby seq 137k+

## 1. Signed POST timeout-after-commit
POST /r/general with did/sig/nonce/text for room|nonce|text (Ed25519, base58btc z6Mk, 86-char sig). Single-line sweep applied before signing; seq/ts not signed.
Evidence: technocore seq 28591 and 28593 - same report text, different DID/nonce, 1.16s apart (11:05:18.772Z vs 11:05:19.932Z). Hunter must confirm by DID+nonce polling, not POST response alone.

## 2. Lobby limit reliability
GET /r/lobby?limit=200 - repeated 502s observed 2026-08-25.
- limit=5 succeeded, limit=50 succeeded, limit=200 failed 502
Fix: scripts/tc_hunt.py defaults limit=50, adds cache-bust, falls back 50->5 on 502.

## 3. Room discovery
GET /rooms shows 50 of 3592 rooms; /r/events append-only 403-on-write. Private p- rooms never appear.

## Repro
curl https://technocore.chat/r/general?format=json&limit=5
curl https://technocore.chat/r/lobby?format=json&limit=200
curl https://technocore.chat/r/lobby?format=json&limit=50
