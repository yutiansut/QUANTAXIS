# QUANTAXIS QAAI - OrcaRouter provider

OrcaRouter is registered here as a **first-class named provider**. QUANTAXIS
ships no other model provider, so this package is the canonical provider seam:
the CLI, the tornado backend and the web panel all bind to it instead of
carrying their own copy of the authentication or discovery logic.

## Two authentication choices, one credential

| provider id | label | credential source |
| --- | --- | --- |
| `orcarouter` | `OrcaRouter - API` | the user pastes an `sk-orca-...` key |
| `orcarouter-oauth` | `OrcaRouter - Auth` | browser authorization (OAuth 2.0 + PKCE) |

Both end at `QAOrcaCredentialProvider` and produce the **same**
`QAOrcaCredentialResult`; the inference adapter and the model catalog read
only `credential.api_key()` and never learn which choice produced it. A
generic "OrcaRouter" button that sometimes asks for a key and sometimes opens
a browser would make logout and reauthentication harder, so the two choices
stay separately testable even though they share a base URL, a model namespace
and a discovery path.

## Origins

Authentication and inference are different public origins and are never
derived from one another:

- consent screen: `https://www.orcarouter.ai/auth`
- code exchange: `https://www.orcarouter.ai/api/v1/auth/keys`
- inference: `https://api.orcarouter.ai/v1`
- model catalog: `https://api.orcarouter.ai/v1/models`

`https://api.orcarouter.ai/v1/auth/keys` is a 404; the paths are pinned as
constants in `QAOrcaEndpoints.py` so no code can compose them by rewriting a
hostname or by appending `/v1`.

Overrides, highest precedence first: `ORCA_AUTH_BASE_URL` /
`ORCA_API_BASE_URL` (explicit), then `ORCA_BASE_URL` (one origin for a
self-hosted deployment), then the public defaults. Remote origins must be
HTTPS; plain HTTP is accepted only for loopback.

## Flow

**Flow B (out-of-band code)** is the primary flow, with **Flow A (loopback
redirect)** implemented for a developer running the CLI on their own
workstation. Flow C (device grant) is not implemented.

QUANTAXIS is self-hosted software: the tornado backend is started with an
arbitrary `--port`/`--address` (`server.py` defaults to `0.0.0.0:8010`) and is
routinely reached over a LAN address or a reverse proxy, so there is no
predictable `127.0.0.1:<port>` a browser could be told to return to. That is
exactly the situation Flow B exists for.

`S256` is sent in both flows, because the consent screen lets the user choose
"show me a code" even when a real `callback_url` was supplied.

## Credential lifecycle

A PKCE exchange returns a **durable OrcaRouter API key, not a refresh
token**. There is no refresh endpoint and nothing here attempts a refresh
grant.

- The key is stored in the QUANTAXIS local setting folder
  (`~/.quantaxis/setting/orcarouter.json`, mode `0600`), created on demand by
  `QUANTAXIS/QASetting/QALocalize.py`. No new secret store is introduced, and
  no plaintext side file is written.
- `ORCAROUTER_API_KEY` still takes precedence, matching the repository's
  existing `MONGOURI`-style environment override convention.
- The stored key is reused across restarts. OrcaRouter caps PKCE-issued keys
  at 10 per user per 24 hours, so re-authorizing on every launch would lock a
  user out.
- A relay `401` flags the **exact account and credential generation** that
  made the rejected request as `needs_reauth`. A late failure from a replaced
  generation cannot mark a newly reauthorized credential broken, and no
  credential is deleted before a successful replacement.

## Model catalog

The only source of truth is `GET {api_base}/v1/models` on the configured
origin, fetched with the user's own key so the result is what that workspace
can actually call. Model identifiers keep their `vendor/model` namespace
verbatim.

Filters, per entry point:

| capability | rule |
| --- | --- |
| chat / agent | `supported_endpoint_types` intersects `openai`, `anthropic`, `gemini`, `openai-response`; records whose types are a subset of `image-generation` / `openai-video` / `jina-rerank` / `embeddings` are excluded |
| multimodal | chat first, then `architecture.input_modalities` must explicitly contain every modality the entry point uploads. Unstated capability fails closed. |
| embedding | `embeddings` endpoint type |
| image | `image-generation` endpoint type |
| video | `openai-video` endpoint type |
| rerank | `jina-rerank` endpoint type |

Requests are bounded (15 s, 4 MiB, 500 items), and a record advertising an
endpoint type this client cannot speak is dropped rather than displayed.

When live discovery fails, a small **verified seed** is served with
`degraded=True` and the error attached, so a catalog outage cannot turn the
selector into a free-text field and a seed is never passed off as the live
list. The seed preserves its verified metadata, including the
`low`/`medium`/`high`/`xhigh` reasoning-effort ladder on `openai/gpt-5.5`.

## Primary-source evidence

Verified 2026-09-11:

| Fact | Source |
| --- | --- |
| OpenAI-compatible inference endpoint | `https://api.orcarouter.ai/v1` (`GET /v1/models` returned 200 with 167 models) |
| Authorization endpoint and code challenge methods | `https://www.orcarouter.ai/.well-known/openid-configuration` — `authorization_endpoint: /auth`, `code_challenge_methods_supported: ["S256","plain"]`, `grant_types_supported: ["authorization_code"]` |
| Token endpoint and "no client secret" | same document — `token_endpoint: /api/v1/auth/keys`, `token_endpoint_auth_methods_supported: ["none"]` |
| Consent screen | `https://www.orcarouter.ai/auth` (HTTP 200) |
| Key revocation / account management | `https://www.orcarouter.ai/console/authorized-apps` (HTTP 200) |

The public defaults above are HTTPS; the discovery document advertises the
same paths over HTTP, so the discovery route is available as an alternative
source of truth for a deployment that prefers not to hardcode them.
