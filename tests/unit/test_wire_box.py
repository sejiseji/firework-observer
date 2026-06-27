from __future__ import annotations

from pyxel_goal_game.camera3d import Camera3D
from pyxel_goal_game.screen_profiles import (
    CLASSIC_PROFILE,
    IPHONE16_BALANCED_PROFILE,
)
from pyxel_goal_game.wire_box import WireBox


def axis_span(values: list[float]) -> float:
    return max(values) - min(values)


def test_classic_wire_box_uses_profile_dimensions() -> None:
    box = WireBox.from_profile(CLASSIC_PROFILE)

    assert axis_span([vertex.x for vertex in box.vertices]) == 120.0
    assert axis_span([vertex.y for vertex in box.vertices]) == 80.0
    assert axis_span([vertex.z for vertex in box.vertices]) == 120.0


def test_iphone16_balanced_wire_box_uses_profile_dimensions() -> None:
    box = WireBox.from_profile(IPHONE16_BALANCED_PROFILE)

    assert axis_span([vertex.x for vertex in box.vertices]) == 120.0
    assert axis_span([vertex.y for vertex in box.vertices]) == 260.0
    assert axis_span([vertex.z for vertex in box.vertices]) == 120.0


def test_wire_box_has_eight_vertices_and_twelve_edges() -> None:
    box = WireBox.from_profile(CLASSIC_PROFILE)

    assert len(box.vertices) == 8
    assert len(box.edges) == 12


def test_wire_box_vertices_are_centered_on_origin() -> None:
    box = WireBox.from_profile(CLASSIC_PROFILE)

    assert sum(vertex.x for vertex in box.vertices) == 0.0
    assert sum(vertex.y for vertex in box.vertices) == 0.0
    assert sum(vertex.z for vertex in box.vertices) == 0.0


def test_wire_box_edge_groups_match_prototype_structure() -> None:
    box = WireBox.from_profile(CLASSIC_PROFILE)

    groups = [edge.group for edge in box.edges]
    assert groups.count("rear") == 4
    assert groups.count("front") == 4
    assert groups.count("connector") == 4


def test_project_edges_uses_camera3d_projection() -> None:
    box = WireBox.from_profile(CLASSIC_PROFILE)
    camera = Camera3D.from_profile(CLASSIC_PROFILE)

    projected_edges = box.project_edges(camera)

    assert len(projected_edges) == 12
    assert all(edge.average_depth > 0.0 for edge in projected_edges)
    assert {edge.group for edge in projected_edges} == {"rear", "front", "connector"}


def test_project_edges_is_deterministic() -> None:
    box = WireBox.from_profile(CLASSIC_PROFILE)
    camera = Camera3D.from_profile(CLASSIC_PROFILE)

    assert box.project_edges(camera) == box.project_edges(camera)
