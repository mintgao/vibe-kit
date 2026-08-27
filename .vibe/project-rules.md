# Project-specific rules

- This repository is the source distribution for Vibe Kit itself.
- Keep the CLI dependency-free and compatible with Python 3.9 or later.
- Treat files selected by `managed_source_files()` in `bin/vibe` as the distributable framework core.
- Add or update scenario tests whenever install, adoption, upgrade, conflict handling, or verification behavior changes.
- Keep network-dependent operations explicit, consent-bound, and covered by an L-sized trust design; local install and packaging remain offline-capable.
