from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from random import Random

from pyxel_goal_game.camera3d import Camera3D, Vec3
from pyxel_goal_game.screen_profiles import ScreenProfile


class BoxStarFace(Enum):
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"
    FRONT = "front"
    BACK = "back"


@dataclass(frozen=True)
class BoxStar:
    position: Vec3
    face: BoxStarFace
    phase: int
    brightness_seed: int


@dataclass(frozen=True)
class BoxStarField:
    stars: tuple[BoxStar, ...]


INWARD_NORMALS = {
    BoxStarFace.TOP: Vec3(0.0, -1.0, 0.0),
    BoxStarFace.LEFT: Vec3(1.0, 0.0, 0.0),
    BoxStarFace.RIGHT: Vec3(-1.0, 0.0, 0.0),
    BoxStarFace.FRONT: Vec3(0.0, 0.0, -1.0),
    BoxStarFace.BACK: Vec3(0.0, 0.0, 1.0),
}
FACE_VISIBILITY_MARGIN = 0.08
TOP_FACE_VISIBILITY_MARGIN = 0.0


def build_box_star_field(
    profile: ScreenProfile,
    seed: int = 20260626,
) -> BoxStarField:
    rng = Random(seed)
    stars: list[BoxStar] = []
    half_width = profile.box_width / 2.0
    half_height = profile.box_height / 2.0
    half_depth = profile.box_depth / 2.0
    inset = 0.98

    for _ in range(36):
        stars.append(
            BoxStar(
                position=Vec3(
                    rng.uniform(-0.90, 0.90) * half_width,
                    inset * half_height,
                    rng.uniform(-0.90, 0.90) * half_depth,
                ),
                face=BoxStarFace.TOP,
                phase=rng.randrange(96),
                brightness_seed=rng.randrange(1024),
            )
        )

    for face in (
        BoxStarFace.LEFT,
        BoxStarFace.RIGHT,
        BoxStarFace.FRONT,
        BoxStarFace.BACK,
    ):
        for _ in range(8):
            stars.append(_side_star(profile, rng, face, inset))

    return BoxStarField(stars=tuple(stars))


def _side_star(
    profile: ScreenProfile,
    rng: Random,
    face: BoxStarFace,
    inset: float,
) -> BoxStar:
    half_width = profile.box_width / 2.0
    half_height = profile.box_height / 2.0
    half_depth = profile.box_depth / 2.0
    y = rng.uniform(0.25, 0.90) * half_height
    if face is BoxStarFace.LEFT:
        position = Vec3(
            -inset * half_width,
            y,
            rng.uniform(-0.88, 0.88) * half_depth,
        )
    elif face is BoxStarFace.RIGHT:
        position = Vec3(
            inset * half_width,
            y,
            rng.uniform(-0.88, 0.88) * half_depth,
        )
    elif face is BoxStarFace.FRONT:
        position = Vec3(
            rng.uniform(-0.88, 0.88) * half_width,
            y,
            inset * half_depth,
        )
    else:
        position = Vec3(
            rng.uniform(-0.88, 0.88) * half_width,
            y,
            -inset * half_depth,
        )
    return BoxStar(
        position=position,
        face=face,
        phase=rng.randrange(96),
        brightness_seed=rng.randrange(1024),
    )


def is_interior_face_visible(camera: Camera3D, face: BoxStarFace) -> bool:
    transformed = camera.transform(INWARD_NORMALS[face])
    if face is BoxStarFace.TOP:
        return transformed.z < TOP_FACE_VISIBILITY_MARGIN
    return transformed.z < -FACE_VISIBILITY_MARGIN


def star_twinkle_color(star: BoxStar, frame_count: int) -> int | None:
    cycle = (frame_count + star.phase) % 96
    if star.brightness_seed % 3 == 0 and 44 <= cycle <= 52:
        return None
    if star.brightness_seed % 7 == 0 and cycle < 8:
        return 7
    if cycle < 18:
        return 6
    if cycle < 58:
        return 5
    return 1
