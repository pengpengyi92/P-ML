# Source and selection protocol

**Title:** Bounded primary-source ML ecosystem curation.
**Date:** 2026-11-15, Asia/Shanghai; exact observations in [snapshot](snapshot.json).

## Scope

The prior10 P-ML cards remain the detailed historical baseline. This expansion starts
with73 declared maintainer-selected upstream projects across15 overlapping routes.
It is not an enumeration of every repository in each organization or every ML project.
There is no star threshold, brand quality score or claim of universal recommendation.

Entries cover learning paradigms, application domains and engineering layers separately.
Canonical redirects are retained alongside requested names. Deduplicate by canonical,
case-insensitive repository ID. Old card observations are dated history, not overwritten
to pretend that earlier commits/PR states were freshly reviewed.

## Primary observations

1. Query public repository metadata, current canonical identity, archive/fork state,
   default-branch commit, root file names/blob IDs and the API's license classifier.
2. Read README and detected root LICENSE/COPYING at the captured commit, not a moving
   branch. Verify UTF-8 byte length and Git blob SHA1; retain SHA256 and pinned URLs.
3. Original learning notes explain role and limits. Generic data/weight/service/third-party
   rights warnings supplement, but do not replace, source-specific license review.
4. Raw responses and source text stay in ignored local review/cache files. Public output
   contains original commentary, metadata, file hashes and links only. No vendor subtree,
   model checkpoints, datasets, private research or user/customer data are published.

GitHub metadata classification is an observed signal, not a version-specific legal
opinion. Missing root license is NEEDS_PERMISSION, not permissive. Multiple file-level
licenses and weight/data cards may differ. Root README/license reads cannot establish
all dependency, dataset, export, patent or commercial-use requirements.

## Failure and freshness policy

Bounded requests, at most2 attempts per query,75-second process timeout. Any transport,
GraphQL, privacy, duplicate, source-integrity or missing-README error stops collection.
An explicit resume can reuse successful cached queries, retaining their original
observation timestamps. The capture is not atomic across projects. Current maintenance
and API compatibility must be checked again before integration.

## Verification is not execution

Offline tests validate schema, unique canonical IDs, fixed source URLs, source hashes,
multi-label dimensions, local navigation, public/private boundaries and negative controls.
An unchanged original experiment is rerun separately. No selected upstream ML runtime,
checkpoint, network inference service, paid compute or installation script is executed.

No accuracy, SOTA, speed, cost reduction, learning gain or production-readiness claim is
made. New experiments require the [fixed protocol](EXPERIMENT_PROTOCOL.md) and their own
measured benchmark card; reading/indexing checks are not a model benchmark.
