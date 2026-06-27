# Scene Policy

## Purpose

Scenes coordinate the active mode of the game.

## Scene responsibilities

A scene may:

- receive input commands,
- update systems,
- request rendering,
- transition to another scene.

A scene should not:

- own low-level particle math,
- own asset baking,
- directly mutate unrelated global state,
- become a dump for all gameplay logic.
