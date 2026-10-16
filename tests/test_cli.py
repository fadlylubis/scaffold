import pytest

from scaffold.cli import available, main, render

EXPECTED = {
    "python/lib",
    "python/fastapi",
    "python/streamlit",
    "python/notebook",
    "python/ml",
    "python/cron",
    "go/service",
    "go/api",
    "go/cron",
    "go/orchestrator",
    "vue/app",
}


def test_all_templates_listed():
    assert set(available()) == EXPECTED


@pytest.mark.parametrize("template", sorted(EXPECTED))
def test_render_replaces_every_token(tmp_path, template):
    target = render(template, "my-app", tmp_path, module="example.com/my-app")
    files = [f for f in target.rglob("*") if f.is_file()]
    assert files
    for f in files:
        assert "__PROJECT__" not in str(f) and "__PACKAGE__" not in str(f)
        assert not f.name.startswith("dot-")
        text = f.read_text()
        for token in ("__PROJECT__", "__PACKAGE__", "__MODULE__"):
            assert token not in text, f"{token} left in {f}"
    assert (target / ".gitignore").exists()


def test_refuses_existing_dir(tmp_path):
    (tmp_path / "taken").mkdir()
    assert main(["new", "python/lib", "taken", "-o", str(tmp_path)]) == 1


def feed(monkeypatch, *answers):
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _: next(it))


def test_plan_reprompts_then_creates(tmp_path, monkeypatch):
    go_api = str(available().index("go/api") + 1)
    # bad choice, valid number, bad name, good name, out dir, default module, default yes
    feed(monkeypatch, "99", go_api, "Bad_Name", "svc", str(tmp_path), "", "")
    assert main(["plan"]) == 0
    assert (tmp_path / "svc/go.mod").read_text().startswith("module github.com/you/svc")


def test_plan_decline_and_ctrl_d(tmp_path, monkeypatch):
    feed(monkeypatch, "python/lib", "lib", str(tmp_path), "n")
    assert main(["plan"]) == 1
    assert not (tmp_path / "lib").exists()

    def eof(_):
        raise EOFError

    monkeypatch.setattr("builtins.input", eof)
    assert main(["plan"]) == 130


def test_rejects_bad_name_and_template(tmp_path):
    assert main(["new", "python/lib", "Bad_Name", "-o", str(tmp_path)]) == 1
    assert main(["new", "rust/cli", "ok", "-o", str(tmp_path)]) == 1
