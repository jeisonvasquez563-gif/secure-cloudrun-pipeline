# ADR 0001: Keyless authentication and signed, digest-pinned deployments

- **Status:** Accepted

## Context

CI/CD pipelines commonly store a Google service-account JSON key as a repository secret. That key is long-lived, easy to leak (logs, forks, compromised dependencies), and rarely rotated. A leak grants persistent access until someone notices.

Deploying images by mutable tag (for example `latest`) also breaks traceability: the tag can point to something different from what the pipeline built and tested.

## Decision

1. **Authenticate with Workload Identity Federation.** GitHub Actions presents its OIDC token and receives short-lived credentials for a dedicated deployer service account. The provider's attribute condition accepts only this repository and only the `main` branch.
2. **Sign the image digest with cosign in keyless mode.** The signing certificate is bound to the workflow identity, so there is no signing key to store or rotate.
3. **Deploy by digest, not by tag.** Cloud Run runs exactly the image that was built and signed.
4. **Scope permissions narrowly.** The deployer can write to one Artifact Registry repository, update one Cloud Run service, and act as one runtime service account. The runtime service account has no roles.
5. **Gate deploys on CI.** The deploy workflow calls the CI workflow and proceeds only if it passes. The `production` environment allows adding required reviewers.

## Consequences

**Positive**
- No credentials to leak or rotate.
- Image provenance can be verified later from the certificate identity.
- A compromised container has no Google API permissions.

**Negative / trade-offs**
- More initial setup (identity pool, provider, bindings) than pasting a key.
- Keyless signing depends on the public Sigstore infrastructure being available.
- Signatures are recorded but not yet **enforced** at deploy time (see the roadmap in the README: Binary Authorization).

## Alternatives considered

- **JSON service-account key as a secret:** rejected for the reasons above.
- **Key-based cosign signing:** rejected; it reintroduces key storage and rotation.
- **Deploying by tag:** rejected; tags are mutable and break traceability.
