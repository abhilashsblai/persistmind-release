# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned Windows release candidate for controlled validation. It is
> not a public beta, production release, or trusted-updater package.

## Release identity

- Version: `0.2.7`
- Release type: Windows Release Candidate
- Source commit: [`210d2ef7dc6421381d823a4a0770667acc679c8a`](https://github.com/abhilashsblai/PersistMind/commit/210d2ef7dc6421381d823a4a0770667acc679c8a)
- Build timestamp: `2026-08-14T03:31:02.511776Z`
- Runtime profile: `windows-stable`
- Distribution: this repository under `releases/0.2.7-candidate`
- Builder environment: Windows 11, CPython 3.13.5
- Production/public beta/officially signed: No

## Download

Use the files committed under
[`releases/0.2.7-candidate`](0.2.7-candidate/README.md). The local installer
expects the root wheel, `dependency-lock.v1.json`, and the sibling CPython 3.13
offline wheelhouse in that directory.

```powershell
cd releases\0.2.7-candidate
$wheelHash = '6dc3283addef93878975060da81f2a0dfa870375fff1570b80e7868180927702'
Get-FileHash .\persistmind-0.2.7-py3-none-any.whl -Algorithm SHA256
Get-FileHash .\dependency-lock.v1.json -Algorithm SHA256
.\install-persistmind.ps1 `
  -BootstrapPath .\bootstrap_persistmind.py `
  -LocalWheelPath .\persistmind-0.2.7-py3-none-any.whl `
  -LocalWheelSha256 $wheelHash `
  -Version 0.2.7
```

The older `0.2.2` GitHub diagnostic wheelhouses remain under
`bundles/0.2.2` for historical controlled validation only.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `persistmind-0.2.7-py3-none-any.whl` | 1,568,226 bytes | `6dc3283addef93878975060da81f2a0dfa870375fff1570b80e7868180927702` |
| `install-persistmind.ps1` | 5,912 bytes | `137c60feb672be0300811b47f63cf926f65440e76c96260fbec76becd13d89f2` |
| `bootstrap_persistmind.py` | 39,279 bytes | `f81e391e783849deca0a6356ff9a536e58494c5334b289a4d161d901d3137d4b` |
| `uninstall_persistmind.py` | 42,262 bytes | `37bdba1077e55efe9b224267764f09d618a5b078f62a78b1e0a899b75745ec5f` |
| `dependency-lock.v1.json` | 12,472 bytes | `d237b60f4a94ac9ec2f63280db0985da5ca230cf47a62756aeb641872a2523aa` |
| `windows-release-build-record.v1.json` | 2,171 bytes | `ddb94fccca2377242375435f915e02094b041f7e72f27c0c5cdadaff91ed0afc` |
| `SHA256SUMS.txt` | 5,375 bytes | `0fcacf7a1579689b8b74aa18f306d1fe41e5f15c63ba62f3bd2cee1115d93154` |

The release folder contains 47 wheels total: the PersistMind root wheel plus
the CPython 3.13 Windows offline dependency wheelhouse recorded by
`dependency-lock.v1.json`.

## Restrictions and known limitations

- Controlled Windows validation only.
- Promotion requires exact installed-artifact and agent evidence.
- The artifact is unsigned and ineligible for `persistmind update`.
- No production, public beta, or SLA claim is made by this candidate.
