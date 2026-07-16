from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pyxel_goal_game.camera3d import Camera3D, ProjectedPoint, Vec3
from pyxel_goal_game.screen_profiles import DEFAULT_SCREEN_PROFILE, ScreenProfile

EdgeGroup = Literal["rear", "front", "connector"]


@dataclass(frozen=True)
class Edge3D:
    start: int
    end: int
    group: EdgeGroup
    is_vertical: bool = False


@dataclass(frozen=True)
class ProjectedEdge:
    start: ProjectedPoint
    end: ProjectedPoint
    average_depth: float
    group: EdgeGroup
    is_vertical: bool = False


@dataclass(frozen=True)
class WireBox:
    vertices: tuple[Vec3, ...]
    edges: tuple[Edge3D, ...]

    @classmethod
    def from_profile(cls, profile: ScreenProfile = DEFAULT_SCREEN_PROFILE) -> WireBox:
        return cls.from_dimensions(
            width=profile.box_width,
            height=profile.box_height,
            depth=profile.box_depth,
        )

    @classmethod
    def from_dimensions(cls, *, width: float, height: float, depth: float) -> WireBox:
        hw = width / 2.0
        hh = height / 2.0
        hd = depth / 2.0
        vertices = (
            Vec3(-hw, -hh, -hd),
            Vec3(hw, -hh, -hd),
            Vec3(hw, hh, -hd),
            Vec3(-hw, hh, -hd),
            Vec3(-hw, -hh, hd),
            Vec3(hw, -hh, hd),
            Vec3(hw, hh, hd),
            Vec3(-hw, hh, hd),
        )
        edges = (
            Edge3D(0, 1, "rear"),
            Edge3D(1, 2, "rear", is_vertical=True),
            Edge3D(2, 3, "rear"),
            Edge3D(3, 0, "rear", is_vertical=True),
            Edge3D(4, 5, "front"),
            Edge3D(5, 6, "front", is_vertical=True),
            Edge3D(6, 7, "front"),
            Edge3D(7, 4, "front", is_vertical=True),
            Edge3D(0, 4, "connector"),
            Edge3D(1, 5, "connector"),
            Edge3D(2, 6, "connector"),
            Edge3D(3, 7, "connector"),
        )
        return cls(vertices=vertices, edges=edges)

    def project_edges(self, camera: Camera3D) -> tuple[ProjectedEdge, ...]:
        projected_vertices = tuple(camera.project(vertex) for vertex in self.vertices)
        return tuple(
            ProjectedEdge(
                start=projected_vertices[edge.start],
                end=projected_vertices[edge.end],
                average_depth=(
                    projected_vertices[edge.start].depth
                    + projected_vertices[edge.end].depth
                )
                / 2.0,
                group=edge.group,
                is_vertical=edge.is_vertical,
            )
            for edge in self.edges
        )
