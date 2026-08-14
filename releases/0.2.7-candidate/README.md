# PersistMind 0.2.7 Windows Release Candidate

> [!WARNING]
> This is an unsigned Windows release candidate for controlled validation. It is
> not a production release, public beta, or trusted-updater package.

## Identity

- Version: `0.2.7`
- Source repository: `abhilashsblai/PersistMind`
- Source commit: `210d2ef7dc6421381d823a4a0770667acc679c8a`
- Release type: Windows Release Candidate
- Runtime profile: `windows-stable`
- Build timestamp: `2026-08-14T03:31:02.511776Z`
- Builder: Windows 11, CPython 3.13.5
- Production/public beta/officially signed: No
- Offline installer target: Windows `win_amd64`, CPython 3.13

## Files

| File | Purpose | SHA-256 |
| --- | --- | --- |
| `persistmind-0.2.7-py3-none-any.whl` | Installable PersistMind wheel | `6dc3283addef93878975060da81f2a0dfa870375fff1570b80e7868180927702` |
| `install-persistmind.ps1` | PowerShell installer | `137c60feb672be0300811b47f63cf926f65440e76c96260fbec76becd13d89f2` |
| `bootstrap_persistmind.py` | Verified bootstrap helper | `f81e391e783849deca0a6356ff9a536e58494c5334b289a4d161d901d3137d4b` |
| `uninstall_persistmind.py` | Project cleanup helper | `37bdba1077e55efe9b224267764f09d618a5b078f62a78b1e0a899b75745ec5f` |
| `dependency-lock.v1.json` | Offline wheelhouse lock for CPython 3.13 | `d237b60f4a94ac9ec2f63280db0985da5ca230cf47a62756aeb641872a2523aa` |
| `windows-release-build-record.v1.json` | Exact build identity record | `ddb94fccca2377242375435f915e02094b041f7e72f27c0c5cdadaff91ed0afc` |
| `SHA256SUMS.txt` | Hash list for committed artifacts | `0fcacf7a1579689b8b74aa18f306d1fe41e5f15c63ba62f3bd2cee1115d93154` |

The directory also contains the sibling CPython 3.13 Windows dependency wheels
required by the local installer. The exact wheelhouse contents are recorded in
`dependency-lock.v1.json`; all file hashes are listed in `SHA256SUMS.txt`.

## Install

From this directory:

```powershell
$wheelHash = '6dc3283addef93878975060da81f2a0dfa870375fff1570b80e7868180927702'
Get-FileHash .\persistmind-0.2.7-py3-none-any.whl -Algorithm SHA256
Get-FileHash .\dependency-lock.v1.json -Algorithm SHA256
.\install-persistmind.ps1 `
  -BootstrapPath .\bootstrap_persistmind.py `
  -LocalWheelPath .\persistmind-0.2.7-py3-none-any.whl `
  -LocalWheelSha256 $wheelHash `
  -Version 0.2.7
```

Then verify:

```powershell
persistmind --version
persistmind --repo C:\Path\To\Repository doctor --summary
```

## Restrictions

- Use only for controlled Windows validation.
- The committed offline wheelhouse is for CPython 3.13 on Windows `win_amd64`.
- Promotion requires installed-artifact evidence and agent evidence.
- This candidate is unsigned and ineligible for trusted `persistmind update`.
- No production, public beta, or SLA claim is made by this artifact.
