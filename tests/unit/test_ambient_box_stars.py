from __future__ import annotations

from pathlib import Path

from pyxel_goal_game.ambient_box_stars import (
    BoxStarFace,
    build_box_star_field,
    is_interior_face_visible,
    star_twinkle_color,
)
from pyxel_goal_game.camera3d import Camera3D
from pyxel_goal_game.screen_profiles import CLASSIC_PROFILE, IPHONE16_BALANCED_PROFILE


def test_box_star_field_is_deterministic() -> None:
    assert build_box_star_field(CLASSIC_PROFILE, seed=1234) == build_box_star_field(
        CLASSIC_PROFILE,
        seed=1234,
    )


def test_box_star_field_changes_with_seed() -> None:
    assert build_box_star_field(CLASSIC_PROFILE, seed=1) != build_box_star_field(
        CLASSIC_PROFILE,
        seed=2,
    )


def test_box_stars_stay_inside_box() -> None:
    for profile in (CLASSIC_PROFILE, IPHONE16_BALANCED_PROFILE):
        field = build_box_star_field(profile)
        half_width = profile.box_width / 2.0
        half_height = profile.box_height / 2.0
        half_depth = profile.box_depth / 2.0

        for star in field.stars:
            assert -half_width <= star.position.x <= half_width
            assert -half_height <= star.position.y <= half_height
            assert -half_depth <= star.position.z <= half_depth


def test_box_stars_are_only_on_top_and_upper_side_faces() -> None:
    field = build_box_star_field(IPHONE16_BALANCED_PROFILE)
    half_height = IPHONE16_BALANCED_PROFILE.box_height / 2.0
    top_y = half_height * 0.98

    assert {star.face for star in field.stars} == {
        BoxStarFace.TOP,
        BoxStarFace.LEFT,
        BoxStarFace.RIGHT,
        BoxStarFace.FRONT,
        BoxStarFace.BACK,
    }
    assert all(star.position.y > 0.0 for star in field.stars)
    assert all(
        star.position.y == top_y
        for star in field.stars
        if star.face is BoxStarFace.TOP
    )
    assert all(
        0.25 * half_height <= star.position.y <= 0.90 * half_height
        for star in field.stars
        if star.face is not BoxStarFace.TOP
    )


def test_box_star_counts_are_modest() -> None:
    field = build_box_star_field(IPHONE16_BALANCED_PROFILE)

    assert sum(1 for star in field.stars if star.face is BoxStarFace.TOP) == 36
    for face in (
        BoxStarFace.LEFT,
        BoxStarFace.RIGHT,
        BoxStarFace.FRONT,
        BoxStarFace.BACK,
    ):
        assert sum(1 for star in field.stars if star.face is face) == 8


def test_interior_face_visibility_uses_camera_orientation() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    camera.yaw = 0.0
    camera.pitch = 0.0

    assert is_interior_face_visible(camera, BoxStarFace.FRONT)
    assert not is_interior_face_visible(camera, BoxStarFace.BACK)
    assert not is_interior_face_visible(camera, BoxStarFace.LEFT)
    assert not is_interior_face_visible(camera, BoxStarFace.RIGHT)


def test_top_interior_visibility_depends_on_pitch() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    camera.yaw = 0.0
    camera.pitch = -0.28

    assert is_interior_face_visible(camera, BoxStarFace.TOP)

    camera.pitch = -0.35

    assert not is_interior_face_visible(camera, BoxStarFace.TOP)


def test_side_face_visibility_keeps_existing_margin() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    camera.pitch = 0.0
    camera.yaw = 0.03

    assert not is_interior_face_visible(camera, BoxStarFace.BACK)
    assert not is_interior_face_visible(camera, BoxStarFace.LEFT)


def test_opposite_side_faces_are_not_both_visible() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    camera.pitch = 0.0
    for yaw in (-1.0, -0.4, 0.0, 0.4, 1.0):
        camera.yaw = yaw

        assert not (
            is_interior_face_visible(camera, BoxStarFace.LEFT)
            and is_interior_face_visible(camera, BoxStarFace.RIGHT)
        )
        assert not (
            is_interior_face_visible(camera, BoxStarFace.FRONT)
            and is_interior_face_visible(camera, BoxStarFace.BACK)
        )


def test_star_twinkle_color_is_deterministic_and_quiet() -> None:
    star = build_box_star_field(CLASSIC_PROFILE, seed=123).stars[0]

    colors = tuple(star_twinkle_color(star, frame) for frame in range(120))

    assert colors == tuple(star_twinkle_color(star, frame) for frame in range(120))
    assert set(colors) <= {None, 1, 5, 6, 7}


def test_ambient_box_stars_module_does_not_import_pyxel() -> None:
    source_lines = Path("src/pyxel_goal_game/ambient_box_stars.py").read_text().splitlines()

    assert "import pyxel" not in source_lines
    assert "from pyxel import" not in source_lines
