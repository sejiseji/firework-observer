from __future__ import annotations


def frame_to_seconds(frame: int, fps: int) -> float:
    if fps <= 0:
        raise ValueError("fps must be positive")
    return frame / fps
