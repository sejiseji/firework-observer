from __future__ import annotations

import math
import random
from dataclasses import dataclass

import pyxel

WIDTH = 256
HEIGHT = 144
FPS = 60

BOX_W = 120.0
BOX_H = 80.0
BOX_D = 120.0

MAX_PARTICLES = 400


@dataclass(frozen=True)
class ProjectedPoint:
    x: float
    y: float
    depth: float

    @property
    def sx(self) -> int:
        return int(round(self.x))

    @property
    def sy(self) -> int:
        return int(round(self.y))


class Camera3D:
    def __init__(self) -> None:
        self.default_yaw = 0.6
        self.default_pitch = 0.3
        self.default_zoom = 1.0

        self.yaw = self.default_yaw
        self.pitch = self.default_pitch
        self.zoom = self.default_zoom
        self.target_yaw = self.default_yaw
        self.target_pitch = self.default_pitch
        self.target_zoom = self.default_zoom

        self.focal = 180.0
        self.camera_distance = 180.0

    def reset(self) -> None:
        self.target_yaw = self.default_yaw
        self.target_pitch = self.default_pitch
        self.target_zoom = self.default_zoom

    def update(self) -> None:
        if pyxel.btn(pyxel.KEY_LEFT):
            self.target_yaw -= 0.035
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.target_yaw += 0.035
        if pyxel.btn(pyxel.KEY_UP):
            self.target_pitch += 0.025
        if pyxel.btn(pyxel.KEY_DOWN):
            self.target_pitch -= 0.025
        if pyxel.btn(pyxel.KEY_A):
            self.target_zoom += 0.018
        if pyxel.btn(pyxel.KEY_S):
            self.target_zoom -= 0.018

        self.target_pitch = clamp(self.target_pitch, -1.05, 1.05)
        self.target_zoom = clamp(self.target_zoom, 0.62, 1.8)

        self.yaw += (self.target_yaw - self.yaw) * 0.12
        self.pitch += (self.target_pitch - self.pitch) * 0.12
        self.zoom += (self.target_zoom - self.zoom) * 0.10

    def project(self, x: float, y: float, z: float) -> ProjectedPoint:
        cos_yaw = math.cos(self.yaw)
        sin_yaw = math.sin(self.yaw)
        cos_pitch = math.cos(self.pitch)
        sin_pitch = math.sin(self.pitch)

        rx = x * cos_yaw - z * sin_yaw
        rz = x * sin_yaw + z * cos_yaw

        ry = y * cos_pitch - rz * sin_pitch
        rz2 = y * sin_pitch + rz * cos_pitch

        depth = max(1.0, rz2 + self.camera_distance)
        scale = self.focal / depth * self.zoom

        sx = WIDTH // 2 + rx * scale
        sy = HEIGHT // 2 - ry * scale
        return ProjectedPoint(sx, sy, depth)


class FireworkBox:
    def __init__(self) -> None:
        hw = BOX_W / 2
        hh = BOX_H / 2
        hd = BOX_D / 2
        self.vertices = [
            (-hw, -hh, -hd),
            (hw, -hh, -hd),
            (hw, hh, -hd),
            (-hw, hh, -hd),
            (-hw, -hh, hd),
            (hw, -hh, hd),
            (hw, hh, hd),
            (-hw, hh, hd),
        ]
        self.edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]

    def draw(self, camera: Camera3D, front: bool | None = None) -> None:
        projected = [camera.project(*vertex) for vertex in self.vertices]
        edge_items = []
        for start, end in self.edges:
            a = projected[start]
            b = projected[end]
            depth = (a.depth + b.depth) * 0.5
            edge_items.append((depth, a, b))

        depths = [item[0] for item in edge_items]
        near = min(depths)
        far = max(depths)
        span = max(1.0, far - near)

        edge_items.sort(key=lambda item: item[0], reverse=True)
        for depth, a, b in edge_items:
            is_front = depth < near + span * 0.42
            if front is not None and is_front != front:
                continue
            color = 13 if is_front else 5
            if not is_front and depth > near + span * 0.78:
                color = 1
            pyxel.line(a.sx, a.sy, b.sx, b.sy, color)


@dataclass
class Rocket:
    x: float
    y: float
    z: float
    prev_x: float
    prev_y: float
    prev_z: float
    vx: float
    vy: float
    vz: float
    target_y: float
    color: int = 10

    @classmethod
    def create(cls) -> Rocket:
        x = random.uniform(-25.0, 25.0)
        y = -BOX_H / 2
        z = random.uniform(-25.0, 25.0)
        return cls(
            x=x,
            y=y,
            z=z,
            prev_x=x,
            prev_y=y,
            prev_z=z,
            vx=random.uniform(-0.045, 0.045),
            vy=random.uniform(1.25, 1.55),
            vz=random.uniform(-0.045, 0.045),
            target_y=random.uniform(5.0, BOX_H / 2 - 10.0),
        )

    def update(self) -> bool:
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_z = self.z

        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.vy -= 0.018
        return self.vy <= 0.0 or self.y >= self.target_y

    def draw(self, camera: Camera3D) -> None:
        prev = camera.project(self.prev_x, self.prev_y, self.prev_z)
        current = camera.project(self.x, self.y, self.z)
        pyxel.line(prev.sx, prev.sy, current.sx, current.sy, 9)
        pyxel.pset(current.sx, current.sy, 7)


@dataclass
class Particle:
    x: float
    y: float
    z: float
    prev_x: float
    prev_y: float
    prev_z: float
    vx: float
    vy: float
    vz: float
    life: int
    max_life: int
    color: int
    fade_mid: int
    fade_dark: int
    tip_color: int
    drag: float
    gravity: float
    has_trail: bool
    trail_until_age: int
    trail_strength: int
    trail_draw_every: int
    depth: float = 0.0

    @property
    def age(self) -> int:
        return self.max_life - self.life

    def update(self) -> bool:
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_z = self.z

        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

        self.vx *= self.drag
        self.vy = self.vy * self.drag + self.gravity
        self.vz *= self.drag

        self.life -= 1
        return self.life <= 0

    def draw(self, camera: Camera3D) -> None:
        current = camera.project(self.x, self.y, self.z)
        previous = camera.project(self.prev_x, self.prev_y, self.prev_z)
        self.depth = current.depth

        color = self.current_color()
        use_trail = (
            self.has_trail
            and self.age < self.trail_until_age
            and pyxel.frame_count % self.trail_draw_every == 0
        )
        if use_trail:
            pyxel.line(previous.sx, previous.sy, current.sx, current.sy, color)
            if self.trail_strength >= 2:
                pyxel.pset(current.sx, current.sy, self.tip_color)
        else:
            pyxel.pset(current.sx, current.sy, color)

    def current_color(self) -> int:
        life_ratio = self.life / self.max_life
        if life_ratio > 0.55:
            return self.color
        if life_ratio > 0.25:
            return self.fade_mid
        return self.fade_dark


class FireworkSystem:
    def __init__(self) -> None:
        self.rockets: list[Rocket] = []
        self.particles: list[Particle] = []

    def launch_kiku(self) -> None:
        self.rockets.append(Rocket.create())

    def update(self) -> None:
        exploding: list[Rocket] = []
        active_rockets: list[Rocket] = []
        for rocket in self.rockets:
            if rocket.update():
                exploding.append(rocket)
            else:
                active_rockets.append(rocket)
        self.rockets = active_rockets

        for rocket in exploding:
            self.create_kiku_explosion(rocket.x, rocket.y, rocket.z)

        self.particles = [
            particle for particle in self.particles if not particle.update()
        ]
        if len(self.particles) > MAX_PARTICLES:
            self.particles = self.particles[-MAX_PARTICLES:]

    def draw(self, camera: Camera3D) -> None:
        for rocket in self.rockets:
            rocket.draw(camera)

        draw_items = []
        for particle in self.particles:
            projected = camera.project(particle.x, particle.y, particle.z)
            particle.depth = projected.depth
            draw_items.append(particle)

        draw_items.sort(key=lambda particle: particle.depth, reverse=True)
        for particle in draw_items:
            particle.draw(camera)

    def create_kiku_explosion(self, x: float, y: float, z: float) -> None:
        count = 112
        for _ in range(count):
            speed = random.uniform(0.90, 1.65)
            vx, vy, vz = random_sphere_velocity(speed)
            life = random.randint(55, 85)
            color = random.choice((10, 9, 7))
            has_trail = speed >= 1.05 and random.random() < 0.32
            trail_strength = 2 if speed >= 1.45 else 1
            self.particles.append(
                Particle(
                    x=x,
                    y=y,
                    z=z,
                    prev_x=x,
                    prev_y=y,
                    prev_z=z,
                    vx=vx,
                    vy=vy,
                    vz=vz,
                    life=life,
                    max_life=life,
                    color=color,
                    fade_mid=9,
                    fade_dark=2,
                    tip_color=7,
                    drag=0.985,
                    gravity=-0.025,
                    has_trail=has_trail,
                    trail_until_age=int(life * 0.48),
                    trail_strength=trail_strength,
                    trail_draw_every=1,
                )
            )
        if len(self.particles) > MAX_PARTICLES:
            self.particles = self.particles[-MAX_PARTICLES:]


class App:
    def __init__(self) -> None:
        pyxel.init(WIDTH, HEIGHT, title="Firework Box", fps=FPS)
        pyxel.mouse(False)
        self.camera = Camera3D()
        self.box = FireworkBox()
        self.fireworks = FireworkSystem()
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_C):
            self.camera.reset()
        if pyxel.btnp(pyxel.KEY_Z):
            self.fireworks.launch_kiku()

        self.camera.update()
        self.fireworks.update()

    def draw(self) -> None:
        pyxel.cls(0)
        draw_background()
        self.box.draw(self.camera, front=False)
        self.fireworks.draw(self.camera)
        self.box.draw(self.camera, front=True)
        self.draw_ui()

    def draw_ui(self) -> None:
        pyxel.text(4, 4, "Z:launch Kiku  ARROWS:rotate", 5)
        pyxel.text(4, 12, "A/S:zoom C:reset", 5)
        pyxel.text(
            4,
            HEIGHT - 8,
            f"particles:{len(self.fireworks.particles):03d} rockets:{len(self.fireworks.rockets)}",
            5,
        )


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def random_sphere_velocity(speed: float) -> tuple[float, float, float]:
    theta = random.uniform(0.0, math.tau)
    u = random.uniform(-1.0, 1.0)
    r = math.sqrt(max(0.0, 1.0 - u * u))
    return math.cos(theta) * r * speed, u * speed, math.sin(theta) * r * speed


def draw_background() -> None:
    pyxel.line(0, HEIGHT // 2 + 30, WIDTH, HEIGHT // 2 + 30, 1)


if __name__ == "__main__":
    App()
