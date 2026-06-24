# Game Concept Hearing Sheet

Use this before initializing or substantially changing the project direction.

The goal is not to answer every question perfectly.
The goal is to prevent Codex from filling important gaps silently.

## 0. Answering rules

For each item, use one of:

- concrete answer
- `unknown`
- `decide later`
- `Codex may propose options`
- `do not include`

If a field affects player experience, prefer a human answer.

---

# 1. Project identity

## 1.1 Basic identity

- Working title:
- Short title:
- Repository/package name:
- One-line pitch:
- Three-line pitch:
- Main genre:
- Sub genre:
- Reference genres:
- Similar games or experiences:
- Anti-reference games or experiences:
- Target platform:
- Target release form:
  - local prototype
  - itch.io
  - browser demo
  - downloadable app
  - internal portfolio
  - paid product
- Target language:
- Target audience:
- Expected session length:
- Expected total play time:
- Is this a prototype, jam game, portfolio piece, or product?

## 1.2 North star

- What should the player feel first?
- What should the player remember after closing the game?
- What is the single most important experience?
- What must never be lost during development?
- What makes this different from a generic Pyxel sample?
- What would make you say “this prototype succeeded”?

---

# 2. Player experience

## 2.1 Desired mood

- Main emotional tone:
- Secondary emotional tone:
- Pace:
  - calm
  - tense
  - rhythmic
  - exploratory
  - chaotic
  - meditative
- Visual density:
  - sparse
  - moderate
  - dense
- Difficulty:
  - no challenge
  - gentle
  - normal
  - hard
  - punishing
- Player pressure:
  - none
  - time pressure
  - survival pressure
  - score pressure
  - puzzle pressure
- Desired aftertaste:
  - relaxing
  - funny
  - mysterious
  - lonely
  - beautiful
  - satisfying
  - unsettling

## 2.2 Player verbs

List the actions the player can do.

- Move:
- Aim:
- Observe:
- Trigger:
- Collect:
- Avoid:
- Build:
- Talk:
- Wait:
- Rotate camera:
- Change viewpoint:
- Choose:
- Other:

For each action:

- Is it core or optional?
- Is it continuous or discrete?
- Does it require timing?
- Does it need visual feedback?
- Does it need sound feedback?

## 2.3 What the player sees

- Main subject on screen:
- Secondary subject:
- Camera style:
  - fixed
  - scrolling
  - free look
  - orbit
  - first-person-like
  - cutout/window view
- View scale:
- Screen resolution:
- Background style:
- Foreground style:
- UI/HUD amount:
- Text amount:
- Animation priority:
- Effects priority:

---

# 3. Game loop

## 3.1 Core loop

Complete this:

1. Player starts by:
2. Player repeatedly:
3. The game responds by:
4. The player improves or progresses by:
5. The loop ends when:

## 3.2 Progression

- Is there progression?
- Stage progression:
- Score progression:
- Collection progression:
- Story progression:
- Skill progression:
- Unlocks:
- Random events:
- Win condition:
- Lose condition:
- Soft ending:
- Hard ending:

## 3.3 Replay value

- Should each run differ?
- Source of variation:
  - random layout
  - random effects
  - random characters
  - player expression
  - score optimization
  - hidden events
- Is deterministic replay useful?
- Should seeds be exposed?

---

# 4. Controls and feel

## 4.1 Input

- Keyboard only?
- Gamepad?
- Mouse?
- Touch?
- Required keys:
- Optional keys:
- Quit key:
- Debug keys:
- Accessibility concerns:

## 4.2 Feel

- Movement feel:
  - grid
  - smooth
  - floaty
  - heavy
  - snappy
- Camera feel:
- Button response:
- Input buffering:
- Acceleration:
- Inertia:
- Screen shake:
- Slow motion:
- Pauses:
- Menu feel:

---

# 5. Visual design

## 5.1 Pyxel constraints

- Use default 16-color palette?
- Custom palette?
- Use `.pyxres`?
- Use generated art?
- Use procedural drawing?
- Use palette animation?
- Use particles?
- Use trails?
- Use tilemap?
- Use sprites?
- Use text?
- Use line/circle primitive drawing?

## 5.2 Art direction

- Pixel-art strictness:
  - strict
  - loose
  - intentionally smooth
  - procedural
- Color mood:
- Main colors:
- Forbidden colors:
- Background complexity:
- Character design:
- Object design:
- Effect design:
- UI design:
- Font/text style:
- Animation style:
- Visual references:
- Anti-references:

## 5.3 Visual risk

- What visual effect is most important?
- What effect may be expensive?
- What can be simplified?
- What must remain beautiful?
- What is acceptable to fake?
- What should be physically accurate?
- What should be emotionally accurate instead?

---

# 6. Audio design

- Use sound effects?
- Use music?
- Use Pyxel built-in sound?
- Sound mood:
- Important sound events:
- Forbidden sound style:
- Volume expectations:
- Is silence acceptable?
- Is rhythm important?
- Does audio affect gameplay?

---

# 7. Content and world

## 7.1 Setting

- World type:
- Place:
- Time:
- Season:
- Weather:
- Main motif:
- Secondary motifs:
- Characters:
- Creatures:
- Objects:
- Story amount:
- Dialogue amount:
- Lore amount:

## 7.2 Narrative policy

- No story?
- Environmental story?
- Dialogue story?
- Ending text?
- Multiple endings?
- Character relationships?
- Tone:
- Things to avoid:

---

# 8. Technical architecture

## 8.1 Project scale

- Expected number of scenes:
- Expected number of systems:
- Expected number of asset types:
- Expected number of levels/stages:
- Save data needed?
- Config needed?
- Debug tools needed?
- Replay tools needed?

## 8.2 Architecture preferences

- Prefer simple files or strict layers?
- Use scene classes?
- Use ECS?
- Use dataclasses?
- Use type hints strictly?
- Use deterministic simulation?
- Use random seed control?
- Separate update/draw strictly?
- Separate model/system/render?
- Keep Pyxel API out of model?
- Allow procedural generation?

## 8.3 Performance budget

- Target FPS:
- Max active particles:
- Max trail length:
- Max enemies/objects:
- Max draw calls concern:
- Resolution:
- Heavy math allowed?
- Precomputation allowed?
- Lookup tables allowed?
- Caching allowed?
- Approximation allowed?

---

# 9. Asset pipeline

- Use Pyxel editor?
- Use external image editor?
- Use generated sprites?
- Use custom sprite tool?
- Use large sprite editing workflow?
- Asset source directory:
- Generated asset directory:
- `.pyxres` policy:
- Sprite size standards:
- Animation frame standards:
- Transparent color:
- Palette rules:
- Naming rules:
- Bake/export command:
- What assets are hand-authored?
- What assets are generated?

---

# 10. Testing and validation

## 10.1 Automated tests

- Unit tests needed for:
- Simulation tests needed for:
- Golden/snapshot tests needed for:
- Smoke tests needed for:
- Import tests needed for:
- Performance checks needed for:

## 10.2 Manual checks

- What must be playtested?
- What must be visually checked?
- What can be checked by screenshot?
- What requires subjective user judgment?
- What is the minimum acceptance checklist?

## 10.3 Regression risks

- What is likely to break?
- What must never regress?
- What can be temporarily broken?
- What needs a TODO rather than immediate fix?

---

# 11. Codex operation

## 11.1 Development style

- Should Codex make proposals before editing?
- Can Codex update docs automatically?
- Can Codex add tests automatically?
- Can Codex refactor?
- Can Codex add dependencies?
- Can Codex change architecture docs?
- Can Codex change task queue?
- Can Codex create ADRs?
- Should Codex stop when product direction is ambiguous?

## 11.2 Task size

- Preferred patch size:
  - tiny
  - small
  - medium
- Maximum files per task:
- Maximum behavior changes per task:
- Should visual and logic changes be separated?
- Should asset changes be separated?

## 11.3 Reporting

Each Codex result should report:

- Summary:
- Files changed:
- Tests run:
- Behavior changed:
- Assumptions:
- Risks:
- User decision needed:
- Suggested next task:

---

# 12. Release and monetization

## 12.1 Release

- Release target:
- Build format:
- itch.io page needed?
- Web version needed?
- Download version needed?
- Versioning style:
- Known issues policy:
- Credits:
- License:
- Source public or private?

## 12.2 Productization

- Is this only a hobby prototype?
- Portfolio goal?
- Paid game?
- Free game with donations?
- Template/tool spin-off?
- Devlog content?
- Screenshot/GIF marketing needed?
- Reusable engine components?
- Reusable asset tools?
- Reusable Codex workflow as product?

---

# 13. Non-goals and boundaries

- Do not implement:
- Do not optimize:
- Do not add:
- Do not support:
- Avoid these themes:
- Avoid these mechanics:
- Avoid these dependencies:
- Avoid these code patterns:
- Avoid this visual direction:
- Avoid this tone:

---

# 14. Initial task generation

After answering, generate:

- Initial `NORTH_STAR.md`
- Initial `GAME_DESIGN.md`
- Initial `PLAYER_EXPERIENCE.md`
- Initial `NON_GOALS.md`
- Initial `ARCHITECTURE_COMPASS.md` additions
- Initial `GOAL_STATE.md`
- Initial `task_queue.json`
- First 3 ExecPlans if needed
- First 5 small Codex tasks
- First smoke checklist
- First playtest checklist
