# Security Policy

## Supported Versions

| Version | Support Level |
|---------|--------------|
| 0.4.x | Full support |
| 0.3.x | Security fixes only |
| < 0.3 | Unsupported |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

To report a security concern, email the maintainers directly. Include:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

## Response Timeline

- **Acknowledgment**: Within 72 hours
- **Assessment**: Within 1 week
- **Fix (if applicable)**: Within 2 weeks for critical issues

## Disclosure Policy

We follow coordinated disclosure:

1. Reporter contacts maintainers privately
2. We assess and develop a fix
3. Fix is released
4. Vulnerability is disclosed publicly after the fix is available

## Security Practices for Contributors

This is an academic research project with a specific security profile:

- **No credentials in code**: Never commit API keys, tokens, or passwords
- **Validate external data**: All corpus data should be validated before processing
- **stdlib-only**: Tools use only Python standard library — no third-party runtime dependencies to audit
- **No user-facing services**: This project does not expose network services; attack surface is limited to local file processing

## Scope

This policy covers the tools, methodology framework, and analysis pipeline. The corpus data itself (Linear A inscriptions) is public academic material and is not subject to security restrictions.
