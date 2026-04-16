import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Soul Foods Pink Morsel Sales Visualiser" in header.text


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)
    graph = dash_duo.find_element("#sales-chart")
    assert graph is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    region_picker = dash_duo.find_element("#region-filter")
    assert region_picker is not None