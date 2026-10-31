# Reporting security vulnerabilities

Security reports are accepted for version 1.0.x. Use private vulnerability reporting
on the repository's Security tab when available. Do not post active tokens,
passwords, or personal data in public issues.

Include the application version, Windows/browser version, steps to reproduce,
and the expected and actual behavior. Use a fresh local account and a test project
when preparing a reproduction.

## Deployment and execution model

DevForge is intended for an individual computer user. Its local HTTP server listens
on `127.0.0.1` and must not be exposed to the internet. User code executes in
restricted Workers. Educational Python packages do not replace a production
FastAPI server or the system Python environment. The terminal runs DevForge's
built-in commands.

Personal data and projects are stored in `%LOCALAPPDATA%/DevForge/data` for Desktop
and `%LOCALAPPDATA%/DevForgeIDE/data` for IDE. They are excluded from the public
repository.
