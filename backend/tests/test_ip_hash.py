import hashlib
import re

import app.ip_hash as ip_hash_module
from app.ip_hash import hash_ip


def test_ip_hash_is_stable_for_same_ip_and_secret(monkeypatch):
    monkeypatch.setattr(
        ip_hash_module.settings, "SECRET_KEY", "test-secret-one"
    )
    assert hash_ip("192.0.2.10") == hash_ip("192.0.2.10")


def test_ip_hash_changes_when_secret_changes(monkeypatch):
    monkeypatch.setattr(
        ip_hash_module.settings, "SECRET_KEY", "test-secret-one"
    )
    first = hash_ip("192.0.2.10")

    monkeypatch.setattr(
        ip_hash_module.settings, "SECRET_KEY", "test-secret-two"
    )
    second = hash_ip("192.0.2.10")

    assert first != second


def test_ip_hash_is_64_lowercase_hex_characters(monkeypatch):
    monkeypatch.setattr(
        ip_hash_module.settings, "SECRET_KEY", "test-secret-one"
    )
    digest = hash_ip("192.0.2.10")

    assert re.fullmatch(r"[0-9a-f]{64}", digest)


def test_ip_hash_does_not_equal_plain_sha256(monkeypatch):
    monkeypatch.setattr(
        ip_hash_module.settings, "SECRET_KEY", "test-secret-one"
    )
    ip = "192.0.2.10"

    assert hash_ip(ip) != hashlib.sha256(
        ip.encode("utf-8")
    ).hexdigest()


def test_ip_hash_changes_when_ip_changes(monkeypatch):
    monkeypatch.setattr(
        ip_hash_module.settings, "SECRET_KEY", "test-secret-one"
    )

    assert hash_ip("192.0.2.10") != hash_ip("192.0.2.11")
