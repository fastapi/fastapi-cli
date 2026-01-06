# Release Notes

## Latest Changes

### Internal

* ⬆ Bump mypy from 1.14.1 to 1.19.1. PR [#261](https://github.com/fastapi/fastapi-cli/pull/261) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update pytest requirement from <9.0.0,>=4.4.0 to >=4.4.0,<10.0.0. PR [#273](https://github.com/fastapi/fastapi-cli/pull/273) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ruff from 0.14.6 to 0.14.10. PR [#262](https://github.com/fastapi/fastapi-cli/pull/262) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/checkout from 5 to 6. PR [#271](https://github.com/fastapi/fastapi-cli/pull/271) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/upload-artifact from 5 to 6. PR [#259](https://github.com/fastapi/fastapi-cli/pull/259) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/download-artifact from 6 to 7. PR [#260](https://github.com/fastapi/fastapi-cli/pull/260) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Add pre-commit workflow. PR [#266](https://github.com/fastapi/fastapi-cli/pull/266) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.0.20

### Features

* ✨ Add --reload-dir option to dev command. PR [#267](https://github.com/fastapi/fastapi-cli/pull/267) by [@patrick91](https://github.com/patrick91).

## 0.0.19

### Breaking Changes

* 🔧 Drop support for Python 3.8. PR [#269](https://github.com/fastapi/fastapi-cli/pull/269) by [@patrick91](https://github.com/patrick91).

## 0.0.18

### Features

* ➕  Add `fastapi-new` in `new` optional dependency group. PR [#241](https://github.com/fastapi/fastapi-cli/pull/241) by [@savannahostrowski](https://github.com/savannahostrowski).

### Fixes

* 🐛 Fix log alignment when pressing Ctrl+C to stop server. PR [#253](https://github.com/fastapi/fastapi-cli/pull/253) by [@savannahostrowski](https://github.com/savannahostrowski).

## 0.0.17

### Upgrades

* ➖ Drop support for Pydantic v1. PR [#268](https://github.com/fastapi/fastapi-cli/pull/268) by [@patrick91](https://github.com/patrick91).

### Internal

* 👷 Configure coverage, error on main tests, don't wait for Smokeshow. PR [#265](https://github.com/fastapi/fastapi-cli/pull/265) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👷 Run Smokeshow always, even on test failures. PR [#264](https://github.com/fastapi/fastapi-cli/pull/264) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#247](https://github.com/fastapi/fastapi-cli/pull/247) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump ruff from 0.14.5 to 0.14.6. PR [#245](https://github.com/fastapi/fastapi-cli/pull/245) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/checkout from 5 to 6. PR [#248](https://github.com/fastapi/fastapi-cli/pull/248) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/checkout from 5 to 6. PR [#244](https://github.com/fastapi/fastapi-cli/pull/244) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Upgrade `latest-changes` GitHub Action and pin `actions/checkout@v5`. PR [#246](https://github.com/fastapi/fastapi-cli/pull/246) by [@svlandeg](https://github.com/svlandeg).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#243](https://github.com/fastapi/fastapi-cli/pull/243) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump ruff from 0.14.4 to 0.14.5. PR [#242](https://github.com/fastapi/fastapi-cli/pull/242) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ✅ Expand test matrix to include Windows and MacOS. PR [#230](https://github.com/fastapi/fastapi-cli/pull/230) by [@svlandeg](https://github.com/svlandeg).
* ⬆ Bump ruff from 0.14.2 to 0.14.4. PR [#239](https://github.com/fastapi/fastapi-cli/pull/239) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#238](https://github.com/fastapi/fastapi-cli/pull/238) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).

## 0.0.16

### Fixes

* 🐛 Fix support for Pydantic v1. PR [#240](https://github.com/fastapi/fastapi-cli/pull/240) by [@patrick91](https://github.com/patrick91).

## 0.0.15

### Features

* ✨ Add support for reading configuration from `pyproject.toml`. PR [#236](https://github.com/fastapi/fastapi-cli/pull/236) by [@patrick91](https://github.com/patrick91).

You can use it in `pyproject.toml` like:

```toml
[tool.fastapi]
entrypoint = "some.importable_module:app_name"
```

### Internal

* ⬆ Bump actions/upload-artifact from 4 to 5. PR [#232](https://github.com/fastapi/fastapi-cli/pull/232) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ruff from 0.14.1 to 0.14.2. PR [#231](https://github.com/fastapi/fastapi-cli/pull/231) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/download-artifact from 5 to 6. PR [#233](https://github.com/fastapi/fastapi-cli/pull/233) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#235](https://github.com/fastapi/fastapi-cli/pull/235) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 🔧 Add PEP-639 license metadata. PR [#234](https://github.com/fastapi/fastapi-cli/pull/234) by [@svlandeg](https://github.com/svlandeg).
* ⬆ Bump astral-sh/setup-uv from 6 to 7. PR [#223](https://github.com/fastapi/fastapi-cli/pull/223) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ruff from 0.13.0 to 0.14.1. PR [#228](https://github.com/fastapi/fastapi-cli/pull/228) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Configure reminder for `waiting` label in `issue-manager`. PR [#227](https://github.com/fastapi/fastapi-cli/pull/227) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#215](https://github.com/fastapi/fastapi-cli/pull/215) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).

## 0.0.14

### Upgrades

* ⬆️ Add support for Python 3.13 and 3.14. PR [#225](https://github.com/fastapi/fastapi-cli/pull/225) by [@svlandeg](https://github.com/svlandeg).

### Internal

* ⬆ Bump tiangolo/issue-manager from 0.5.1 to 0.6.0. PR [#220](https://github.com/fastapi/fastapi-cli/pull/220) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.0.13

### Features

* ✨ Allow to use `-h` for help. PR [#191](https://github.com/fastapi/fastapi-cli/pull/191) by [@patrick91](https://github.com/patrick91).

## 0.0.12

### Features

* ✨ Add support for the PORT environment variable. PR [#209](https://github.com/fastapi/fastapi-cli/pull/209) by [@buurro](https://github.com/buurro).

### Internal

* ⬆ Bump mypy from 1.14.0 to 1.14.1. PR [#207](https://github.com/fastapi/fastapi-cli/pull/207) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/setup-python from 5 to 6. PR [#201](https://github.com/fastapi/fastapi-cli/pull/201) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ruff from 0.12.12 to 0.13.0. PR [#206](https://github.com/fastapi/fastapi-cli/pull/206) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#208](https://github.com/fastapi/fastapi-cli/pull/208) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#205](https://github.com/fastapi/fastapi-cli/pull/205) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).

## 0.0.11

### Features

* ✨ Add support for passing apps as `fastapi run --entrypoint some.importable_module:app_name`. PR [#199](https://github.com/fastapi/fastapi-cli/pull/199) by [@patrick91](https://github.com/patrick91).

If you have been using Uvicorn like:

```console
$ uvicorn some.importable_module:app_name
```

Now you can use the same "entrypoint" syntax with `fastapi`:

```console
$ fastapi run -e some.importable_module:app_name
```

Or:

```console
$ fastapi run --entrypoint some.importable_module:app_name
```

### Internal

* ⬆ Bump actions/labeler from 5 to 6. PR [#202](https://github.com/fastapi/fastapi-cli/pull/202) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ruff from 0.12.11 to 0.12.12. PR [#203](https://github.com/fastapi/fastapi-cli/pull/203) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#198](https://github.com/fastapi/fastapi-cli/pull/198) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.12.4 to 1.13.0. PR [#200](https://github.com/fastapi/fastapi-cli/pull/200) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Detect and label merge conflicts on PRs automatically. PR [#204](https://github.com/fastapi/fastapi-cli/pull/204) by [@svlandeg](https://github.com/svlandeg).

## 0.0.10

### Features

* Add CLI option `--forwarded-allow-ips`. PR [#113](https://github.com/fastapi/fastapi-cli/pull/113) by [@Riuzaky77](https://github.com/Riuzaky77).

### Internal

* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#147](https://github.com/fastapi/fastapi-cli/pull/147) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump ruff from 0.11.2 to 0.12.11. PR [#196](https://github.com/fastapi/fastapi-cli/pull/196) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/checkout from 4 to 5. PR [#193](https://github.com/fastapi/fastapi-cli/pull/193) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/download-artifact from 4 to 5. PR [#190](https://github.com/fastapi/fastapi-cli/pull/190) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump tiangolo/latest-changes from 0.3.2 to 0.4.0. PR [#188](https://github.com/fastapi/fastapi-cli/pull/188) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump astral-sh/setup-uv from 5 to 6. PR [#176](https://github.com/fastapi/fastapi-cli/pull/176) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.0.9

### Fixes

* 🔧 Remove command script `fastapi`, let it be provided by the `fastapi` package. PR [#197](https://github.com/fastapi/fastapi-cli/pull/197) by [@tiangolo](https://github.com/tiangolo).

## 0.0.8

### Features

* ➕ Add optional dependency on `fastapi-cloud-cli`. PR [#181](https://github.com/fastapi/fastapi-cli/pull/181) by [@tiangolo](https://github.com/tiangolo).

This will allow you to deploy to [FastAPI Cloud](https://fastapicloud.com) with the `fastapi deploy` command.

Installing `fastapi-cli[standard]` now includes `fastapi-cloud-cli`.

If you want to install `fastapi-cli` without `fastapi-cloud-cli`, you can install instead `fastapi-cli[standard-no-fastapi-cloud-cli]`.

You will normally not install `fastapi-cli` directly, but rather install FastAPI with `fastapi[standard]`, which will include `fastapi-cli[standard]`.

If you want to install `fastapi` with the standard dependencies except for `fastapi-cloud-cli`, you can install instead `fastapi[standard-no-fastapi-cloud-cli]`.

### Internal

* ⬆ Bump pypa/gh-action-pypi-publish from 1.12.3 to 1.12.4. PR [#152](https://github.com/fastapi/fastapi-cli/pull/152) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ruff from 0.8.4 to 0.11.2. PR [#168](https://github.com/fastapi/fastapi-cli/pull/168) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#138](https://github.com/fastapi/fastapi-cli/pull/138) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump ruff from 0.8.2 to 0.8.4. PR [#139](https://github.com/fastapi/fastapi-cli/pull/139) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump astral-sh/setup-uv from 4 to 5. PR [#140](https://github.com/fastapi/fastapi-cli/pull/140) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mypy from 1.13.0 to 1.14.0. PR [#141](https://github.com/fastapi/fastapi-cli/pull/141) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.0.7

### Fixes

* 🐛 Do not disable existing loggers. PR [#132](https://github.com/fastapi/fastapi-cli/pull/132) by [@kraftp](https://github.com/kraftp).

### Internal

* 🚨 Format new test. PR [#137](https://github.com/fastapi/fastapi-cli/pull/137) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.12.2 to 1.12.3. PR [#134](https://github.com/fastapi/fastapi-cli/pull/134) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#62](https://github.com/fastapi/fastapi-cli/pull/62) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump ruff from 0.5.5 to 0.8.1. PR [#128](https://github.com/fastapi/fastapi-cli/pull/128) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.0.6

### Features

* ✨ Improve UI for `fastapi dev` and `fastapi run`. PR [#95](https://github.com/fastapi/fastapi-cli/pull/95) by [@patrick91](https://github.com/patrick91).

### Fixes

* 🐛 Use correct syntax for links. PR [#131](https://github.com/fastapi/fastapi-cli/pull/131) by [@patrick91](https://github.com/patrick91).

### Internal

* 👷 Update `labeler.yml`. PR [#101](https://github.com/fastapi/fastapi-cli/pull/101) by [@tiangolo](https://github.com/tiangolo).
* 👷 Do not sync labels as it overrides manually added labels. PR [#71](https://github.com/fastapi/fastapi-cli/pull/71) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Use ruff check command in format script. PR [#121](https://github.com/fastapi/fastapi-cli/pull/121) by [@FlavienRx](https://github.com/FlavienRx).
* ⬆ Update pre-commit requirement from <4.0.0,>=2.17.0 to >=2.17.0,<5.0.0. PR [#100](https://github.com/fastapi/fastapi-cli/pull/100) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.9.0 to 1.12.2. PR [#117](https://github.com/fastapi/fastapi-cli/pull/117) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump tiangolo/latest-changes from 0.3.1 to 0.3.2. PR [#118](https://github.com/fastapi/fastapi-cli/pull/118) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump astral-sh/setup-uv from 3 to 4. PR [#125](https://github.com/fastapi/fastapi-cli/pull/125) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mypy from 1.11.1 to 1.13.0. PR [#111](https://github.com/fastapi/fastapi-cli/pull/111) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Fix smokeshow, checkout files on CI. PR [#106](https://github.com/fastapi/fastapi-cli/pull/106) by [@tiangolo](https://github.com/tiangolo).
* 👷 Use uv in CI. PR [#105](https://github.com/fastapi/fastapi-cli/pull/105) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update `labeler.yml`. PR [#102](https://github.com/fastapi/fastapi-cli/pull/102) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump tiangolo/issue-manager from 0.5.0 to 0.5.1. PR [#89](https://github.com/fastapi/fastapi-cli/pull/89) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update `issue-manager.yml`. PR [#88](https://github.com/fastapi/fastapi-cli/pull/88) by [@tiangolo](https://github.com/tiangolo).
* 💚 Set `include-hidden-files` to `True` when using the `upload-artifact` GH action. PR [#84](https://github.com/fastapi/fastapi-cli/pull/84) by [@svlandeg](https://github.com/svlandeg).
* 👷 Update `latest-changes` GitHub Action. PR [#79](https://github.com/fastapi/fastapi-cli/pull/79) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update coverage configs. PR [#74](https://github.com/fastapi/fastapi-cli/pull/74) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add URLs to `pyproject.toml`, show up in PyPI. PR [#72](https://github.com/fastapi/fastapi-cli/pull/72) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action labeler to only add one label. PR [#70](https://github.com/fastapi/fastapi-cli/pull/70) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action labeler permissions and dependencies. PR [#69](https://github.com/fastapi/fastapi-cli/pull/69) by [@tiangolo](https://github.com/tiangolo).
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
