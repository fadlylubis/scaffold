from streamlit.testing.v1 import AppTest


def test_app_runs():
    at = AppTest.from_file("../app.py", default_timeout=30).run()
    assert not at.exception
