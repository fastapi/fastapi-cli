# Release Notes

## Latest Changes

### Internal

* 👷 Add GitHub Action label-checker. PR [#68](https://github.com/fastapi/fastapi-cli/pull/68) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action labeler. PR [#67](https://github.com/fastapi/fastapi-cli/pull/67) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update GitHub Action add-to-project. PR [#66](https://github.com/fastapi/fastapi-cli/pull/66) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action add-to-project. PR [#65](https://github.com/fastapi/fastapi-cli/pull/65) by [@tiangolo](https://github.com/tiangolo).

## 0.0.5

### Breaking Changes

* ♻️ Add `fastapi-cli[standard]` including Uvicorn, make `fastapi-cli` and `fastapi-cli-slim` have the same packages. PR [#55](https://github.com/fastapi/fastapi-cli/pull/55) by [@tiangolo](https://github.com/tiangolo).
* ➕ Keep Uvicorn in default dependencies. PR [#57](https://github.com/fastapi/fastapi-cli/pull/57) by [@tiangolo](https://github.com/tiangolo).

#### Summary

Install with:

```bash
pip install "fastapi[standard]"
```

Or if for some reason installing only the FastAPI CLI:

```bash
pip install "fastapi-cli[standard]"
```

#### Technical Details

Before this, `fastapi-cli` would include Uvicorn and `fastapi-cli-slim` would not include Uvicorn.

In a future version, `fastapi-cli` will not include Uvicorn unless it is installed with `fastapi-cli[standard]`.

FastAPI version 0.112.0 has a `fastapi[standard]` and that one includes `fastapi-cli[standard]`.

Before, you would install `pip install fastapi`, or `pip install fastapi-cli`. Now you should include the `standard` optional dependencies (unless you want to exclude one of those): `pip install "fastapi[standard]"`.

In a future version, `fastapi-cli` will not include Uvicorn unless it is installed with `fastapi-cli[standard]`.

### Refactors

* ♻️ Simplify code in `src/fastapi_cli/discover.py`. PR [#22](https://github.com/tiangolo/fastapi-cli/pull/22) by [@pedroimpulcetto](https://github.com/pedroimpulcetto).

### Docs

* 🚚 Rename repo references to new GitHub FastAPI org. PR [#56](https://github.com/fastapi/fastapi-cli/pull/56) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump ruff from 0.4.5 to 0.5.5. PR [#52](https://github.com/fastapi/fastapi-cli/pull/52) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Remove Python 3.7 from PyPI classifiers. PR [#48](https://github.com/fastapi/fastapi-cli/pull/48) by [@patrick91](https://github.com/patrick91).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#28](https://github.com/fastapi/fastapi-cli/pull/28) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump mypy from 1.10.0 to 1.11.1. PR [#53](https://github.com/fastapi/fastapi-cli/pull/53) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.8.14 to 1.9.0. PR [#34](https://github.com/fastapi/fastapi-cli/pull/34) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update issue-manager.yml GitHub Action permissions. PR [#54](https://github.com/tiangolo/fastapi-cli/pull/54) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump ruff from 0.4.4 to 0.4.5. PR [#29](https://github.com/tiangolo/fastapi-cli/pull/29) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ruff from 0.4.3 to 0.4.4. PR [#23](https://github.com/tiangolo/fastapi-cli/pull/23) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Enable CI tests for Python 3.12. PR [#27](https://github.com/tiangolo/fastapi-cli/pull/27) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update Upload/Download artifacts GitHub Actions. PR [#26](https://github.com/tiangolo/fastapi-cli/pull/26) by [@tiangolo](https://github.com/tiangolo).

## 0.0.4

### Fixes

* 🔧 Make FastAPI and Uvicorn optional dependencies, to avoid circular dependencies. PR [#25](https://github.com/tiangolo/fastapi-cli/pull/25) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump actions/cache from 3 to 4. PR [#5](https://github.com/tiangolo/fastapi-cli/pull/5) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.8.11 to 1.8.14. PR [#2](https://github.com/tiangolo/fastapi-cli/pull/2) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.0.3

### Features

* ✨ Add optional `--workers` CLI option, and fix CI for test-redistribute. PR [#12](https://github.com/tiangolo/fastapi-cli/pull/12) by [@PokkaKiyo](https://github.com/PokkaKiyo).

### Upgrades

* ➖ Relax Uvicorn pin. PR [#16](https://github.com/tiangolo/fastapi-cli/pull/16) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Add note about Uvicorn as the high-performance server running underneath. PR [#9](https://github.com/tiangolo/fastapi-cli/pull/9) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump ruff from 0.2.0 to 0.4.3. PR [#14](https://github.com/tiangolo/fastapi-cli/pull/14) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update pytest requirement from <8.0.0,>=4.4.0 to >=4.4.0,<9.0.0. PR [#4](https://github.com/tiangolo/fastapi-cli/pull/4) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mypy from 1.4.1 to 1.10.0. PR [#7](https://github.com/tiangolo/fastapi-cli/pull/7) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.0.2

First public working version. 🚀

### Fixes

* 👷 Tweak CI testing and fix import error detection for Python 3.8. PR [#8](https://github.com/tiangolo/fastapi-cli/pull/8) by [@tiangolo](https://github.com/tiangolo).
