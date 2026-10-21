#!/usr/bin/env python3
"""Launch a LAN opponent that picks a random fighter and uses the game's AI.

The human starts the same mode in Dragon Net Battle with BT3_LAN=host.
"""

import argparse
import os
from pathlib import Path
import signal
import subprocess


ROOT = Path(__file__).resolve().parents[2]
MODES = {
    "1v1": "S",
    "team": "T",
    "dp10": "D10",
    "dp15": "D15",
    "dp20": "D20",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=MODES, help="optional mode to start immediately")
    parser.add_argument("--host", default="127.0.0.1", help="address of the human player's game")
    parser.add_argument("--name", default="Sparking Bot", help="name shown to the other player")
    parser.add_argument("--level", type=int, choices=range(1, 6), default=3,
                        metavar="1-5", help="CPU difficulty, 1 easiest and 5 hardest (default: 3)")
    parser.add_argument("--game", type=Path, default=ROOT / "port/build/bt3_64", help="built game executable")
    args = parser.parse_args()
    game = args.game.resolve()
    if not game.is_file():
        parser.error(f"game executable not found: {game}")
    if ":" in args.host or not args.host:
        parser.error("--host must be an IPv4 address or hostname without a port")

    process: subprocess.Popen[bytes] | None = None
    selected_level = args.level
    current_mode: str | None = None

    def stop_game() -> None:
        nonlocal process
        if process is None:
            return
        if process.poll() is None:
            try:
                if os.name == "posix":
                    os.killpg(process.pid, signal.SIGTERM)
                else:
                    process.terminate()
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    if os.name == "posix":
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                except ProcessLookupError:
                    pass
                process.wait()
        process = None

    def start_game(mode: str) -> None:
        nonlocal process, current_mode
        stop_game()
        env = os.environ.copy()
        for name in ("BT3_REPLAY", "BT3_DEMO", "BT3_NET_HOST", "BT3_NET_JOIN", "BT3_LOBBY"):
            env.pop(name, None)
        env["BT3_NET_BOT"] = "1"
        env["BT3_NET_BOT_LEVEL"] = str(selected_level - 1)
        env["BT3_NET_NAME"] = args.name
        env["BT3_LOBBY"] = f"lan:join:{args.host}:{MODES[mode]}"
        env["BT3_GS"] = "none"
        env["BT3_NOSOUND"] = "1"
        process = subprocess.Popen([str(game)], cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                                   start_new_session=os.name == "posix")
        current_mode = mode
        print(f"Headless bot running in {mode} mode at CPU level {selected_level}, joining {args.host}.", flush=True)

    help_text = "Commands: 1v1, team, dp10, dp15, dp20, level 1-5, exit"
    print(help_text, flush=True)
    try:
        if args.mode is not None:
            start_game(args.mode)
        while True:
            try:
                command = input("bot> ").strip().lower()
            except EOFError:
                break
            if command in ("exit", "quit"):
                break
            words = command.split()
            if not words:
                continue
            if words[0] == "level" and len(words) == 2 and words[1] in ("1", "2", "3", "4", "5"):
                selected_level = int(words[1])
                if current_mode is not None:
                    start_game(current_mode)
                else:
                    print(f"CPU level set to {selected_level}")
            elif words[0] in MODES and len(words) in (1, 2) and (len(words) == 1 or words[1] in ("1", "2", "3", "4", "5")):
                if len(words) == 2:
                    selected_level = int(words[1])
                start_game(words[0])
            elif command == "help":
                print(help_text)
            elif command:
                print(f"Unknown command: {command}. Type help for available commands.")
    except KeyboardInterrupt:
        print()
    finally:
        stop_game()


if __name__ == "__main__":
    main()
