"""Pick a measurement backend by file suffix. Today only Python."""

from __future__ import annotations

from pathlib import Path

from maintainability.languages import python as py
from maintainability.model import Corpus, Mod
from maintainability.registry import BoundAuthority

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
    ".pytest_cache",
}

def build_corpus(root: Path, code_roots: tuple[Path, ...], exclude: tuple[Path, ...]) -> Corpus:
    root = root.resolve()
    import_roots = py.discover_import_roots(root)
    files: list[Path] = []
    for base in code_roots:
        if not base.exists():
            continue
        if base.is_file() and base.suffix == py.SUFFIX:
            rp = base.resolve()
            if not _excluded(rp, exclude):
                files.append(rp)
            continue
        for p in base.rglob(f"*{py.SUFFIX}"):
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            rp = p.resolve()
            if _excluded(rp, exclude):
                continue
            files.append(rp)
    files = sorted(set(files))
    modules: list[Mod] = []
    by_path: dict[Path, Mod] = {}
    symbols: list[tuple[str, str, Path]] = []
    for path in files:
        if path.suffix != py.SUFFIX:
            continue
        mod = py.parse_file(path, root, import_roots)
        if mod is None:
            continue
        modules.append(mod)
        by_path[path] = mod
        if mod.language == py.LANGUAGE:
            for qname, doc in py.symbol_docs(mod):
                symbols.append((qname, doc, path))
        else:
            symbols.append((mod.qname, "", path))
    corpus = Corpus(root=root, modules=modules, by_path=by_path, symbols=symbols)
    py.resolve_corpus(corpus)
    return corpus


def default_entry_paths(root: Path) -> list[Path]:
    return py.default_entry_paths(root.resolve(), SKIP_DIRS)


def seed_members(mod: Mod) -> set[str]:
    if mod.language == py.LANGUAGE:
        return py.seed_members(mod)
    return set()


def token_hits(mod: Mod, members: set[str]) -> list[tuple[int, str, str]]:
    if mod.language == py.LANGUAGE:
        return py.token_hits(mod, members)
    return []


def authority_aliases(corpus: Corpus, auth: BoundAuthority) -> dict[Path, set[str]]:
    return py.authority_aliases(corpus, auth)


def is_use(mod: Mod, lineno: int, token: str, aliases: dict[Path, set[str]], auth_qname: str) -> bool:
    if mod.language == py.LANGUAGE:
        return py.is_use(mod, lineno, token, aliases, auth_qname)
    return False


def attr_is_use(mod: Mod, lineno: int, aliases: dict[Path, set[str]]) -> bool:
    if mod.language == py.LANGUAGE:
        return py.attr_is_use(mod, lineno, aliases)
    return False


def string_in_use_context(mod: Mod, lineno: int, aliases: dict[Path, set[str]]) -> bool:
    if mod.language == py.LANGUAGE:
        return py.string_in_use_context(mod, lineno, aliases)
    return False


def mentions(mod: Mod, auth: BoundAuthority) -> bool:
    if mod.language == py.LANGUAGE:
        return py.mentions(mod, auth)
    return False


def reads_authority(mod: Mod, auth: BoundAuthority) -> bool:
    if mod.language == py.LANGUAGE:
        return py.reads_authority(mod, auth)
    return False


def fail_loud_matches(corpus: Corpus, auth_qname: str, auth_mod: Mod | None):
    return py.fail_loud_matches(corpus, auth_qname, auth_mod)


def _excluded(path: Path, exclude: tuple[Path, ...]) -> bool:
    for ex in exclude:
        try:
            path.relative_to(ex)
            return True
        except ValueError:
            continue
    return False
