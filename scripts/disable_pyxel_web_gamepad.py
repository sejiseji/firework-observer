from __future__ import annotations

import argparse
from pathlib import Path

ENABLED_GAMEPAD = 'gamepad: "enabled"'
DISABLED_GAMEPAD = 'gamepad: "disabled"'
PYXEL_SCRIPT_TAG = (
    '<script src="https://cdn.jsdelivr.net/gh/kitao/pyxel@2.9.6/wasm/pyxel.js">'
    "</script>"
)
SAFARI_AUDIO_UNLOCK_MARKER = "__fireworkObserverAudioUnlockInstalled"
SAFARI_AUDIO_UNLOCK_SCRIPT = f"""<script>
(function () {{
  if (window.{SAFARI_AUDIO_UNLOCK_MARKER}) {{
    return;
  }}
  window.{SAFARI_AUDIO_UNLOCK_MARKER} = true;

  var contexts = [];

  function rememberContext(context) {{
    if (contexts.indexOf(context) === -1) {{
      contexts.push(context);
    }}
    return context;
  }}

  function patchAudioContext(name) {{
    var OriginalAudioContext = window[name];
    if (!OriginalAudioContext || OriginalAudioContext.__fireworkObserverPatched) {{
      return;
    }}

    function PatchedAudioContext(options) {{
      var context = options === undefined
        ? new OriginalAudioContext()
        : new OriginalAudioContext(options);
      return rememberContext(context);
    }}

    PatchedAudioContext.prototype = OriginalAudioContext.prototype;
    Object.setPrototypeOf(PatchedAudioContext, OriginalAudioContext);
    PatchedAudioContext.__fireworkObserverPatched = true;
    window[name] = PatchedAudioContext;
  }}

  function playSilentTick(context) {{
    if (!context || !context.createBuffer || !context.createBufferSource) {{
      return;
    }}
    try {{
      var buffer = context.createBuffer(1, 1, 22050);
      var source = context.createBufferSource();
      source.buffer = buffer;
      source.connect(context.destination);
      source.start(0);
    }} catch (error) {{
      // Best-effort Safari audio unlock. Runtime audio can still retry from Python.
    }}
  }}

  function unlockAudio() {{
    var AudioContextConstructor = window.AudioContext || window.webkitAudioContext;
    if (AudioContextConstructor && contexts.length === 0) {{
      try {{
        new AudioContextConstructor();
      }} catch (error) {{
        // Ignore and try again on the next user gesture.
      }}
    }}

    contexts.forEach(function (context) {{
      if (!context) {{
        return;
      }}
      if (context.state === "suspended" && context.resume) {{
        try {{
          context.resume();
        }} catch (error) {{
          // Ignore and try again on the next user gesture.
        }}
      }}
      playSilentTick(context);
    }});
  }}

  patchAudioContext("AudioContext");
  patchAudioContext("webkitAudioContext");

  ["touchstart", "pointerdown", "mousedown", "keydown"].forEach(function (eventName) {{
    window.addEventListener(eventName, unlockAudio, {{ capture: true, passive: true }});
  }});
}})();
</script>"""


def disable_pyxel_web_gamepad(html: str) -> str:
    if DISABLED_GAMEPAD in html:
        return html
    if ENABLED_GAMEPAD not in html:
        msg = "Pyxel web gamepad setting was not found"
        raise ValueError(msg)
    return html.replace(ENABLED_GAMEPAD, DISABLED_GAMEPAD, 1)


def install_safari_audio_unlock(html: str) -> str:
    if SAFARI_AUDIO_UNLOCK_MARKER in html:
        return html
    if PYXEL_SCRIPT_TAG not in html:
        msg = "Pyxel web script tag was not found"
        raise ValueError(msg)
    return html.replace(
        PYXEL_SCRIPT_TAG,
        f"{PYXEL_SCRIPT_TAG}\n{SAFARI_AUDIO_UNLOCK_SCRIPT}",
        1,
    )


def patch_pyxel_web_html(html: str) -> str:
    return install_safari_audio_unlock(disable_pyxel_web_gamepad(html))


def patch_file(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    patched = patch_pyxel_web_html(html)
    path.write_text(patched, encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Patch generated Pyxel Web HTML for public release.",
    )
    parser.add_argument("html_file", type=Path)
    args = parser.parse_args(argv)
    patch_file(args.html_file)


if __name__ == "__main__":
    main()
