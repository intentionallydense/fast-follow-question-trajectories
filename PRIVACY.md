# Public-release privacy review

This repository is a **privacy-sanitized derivative** of the locally retained audit bundle. The repository was kept private during review. The original source archive and original audit artifacts remain outside this public repository in the owner's local workspace.

## Removed from this release

- API-key, access-token and other credential-like URL query values, including nested and multiply URL-encoded proxy URLs. These included Census, DPLA, UNCTAD and Preservica references. Demo keys were also removed conservatively.
- Signed Google document-viewer identifiers, nonces and validation hashes.
- Two distinct full IP addresses and 19,913 `ip16` metadata values. Aggregate counts are retained.
- Local usernames in filesystem paths; `/home/public` and `/home/run` are placeholders.

No provider-specific access tokens, private keys, personal email addresses or phone numbers were identified in the content review. The apparent email match was a URL-routing experiment, not a person's contact address. Human handles in the supplied archive were already anonymized. Reported agent signatures, benchmark dates, public source URLs and public GitHub account information remain as research context.

## Effect on evidence

Credential/address replacements preserve character lengths. Source-span offsets and revision IDs therefore remain usable. Span hashes, source-body hashes, archive member checksums, active review gates and the release file manifest have been updated for the sanitized contents. The current release retains 298 supported histories and 24 provisional entries, including the CVD expansion; privacy redaction does not change their membership or round/event counts.

For the CVD update, all 410 referenced revision bodies were compared with this sanitized archive; none differed from their locally reviewed bodies. IP-prefix metadata was removed from the added research records, and the CVD acceptance gate was refreshed against the sanitized inputs. The original unsanitized archive and Sites hosting configuration were not copied into the release.

The archive retains the filename `full-wiki-logs.zip` so existing exporters work, but **it is no longer the original byte-exact archive**. Its member manifest explicitly identifies the derivative. “Original” and historical checks in older audit reports refer to the pre-redaction review stage. Some historical provenance hashes intentionally identify those earlier inputs; the top-level `MANIFEST.json` and active public-release validation cover the published files. Recorded semantic audits predate redaction; refreshed gate hashes do not claim a new semantic audit.

## Checks

The initial release was reviewed with independent manual inspection and pattern scans of every tracked file and every archive member, including decoded URL parameters. Checks did not submit any candidate credentials to external services. The CVD update reruns the privacy scanner, data exporters, source/citation validation and thirteen data tests after preserving those redactions.

```sh
python privacy_check.py
python validate_bundle.py
```

The automated privacy checker covers the specific credential and address classes found during review. This is a documented review, not a guarantee that arbitrary source text can never contain sensitive information.
