#!/usr/bin/env python3
"""
Драйвер сеансу sqlite3 для практичної роботи 2.

Запускає справжній sqlite3 у псевдотерміналі (pty), послідовно "друкує"
команди та збирає автентичний транскрипт консолі покроково.
Кожен крок зберігається окремим .txt-логом (далі з нього робиться скріншот).
"""
import os
import pty
import re
import select
import signal
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(BASE, "logs")

ANSI = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b[()][B0]|\x1b[=>]|\x07")


class SqliteSession:
    def __init__(self, dbfile, cwd):
        self.master, slave = pty.openpty()
        import termios
        attrs = termios.tcgetattr(slave)
        attrs[1] = attrs[1] & ~termios.ONLCR          # без зайвого перетворення NL
        termios.tcsetattr(slave, termios.TCSANOW, attrs)
        self.pid = os.fork()
        if self.pid == 0:                              # дочірній процес
            os.setsid()
            os.dup2(slave, 0)
            os.dup2(slave, 1)
            os.dup2(slave, 2)
            os.close(self.master)
            os.close(slave)
            os.chdir(cwd)
            env = dict(os.environ, TERM="dumb", LINES="40", COLUMNS="100")
            os.execvpe("sqlite3", ["sqlite3", dbfile], env)
            os._exit(127)
        os.close(slave)

    def read_idle(self, idle=0.45, timeout=12.0):
        """Читає з pty, доки потік не затихне на `idle` секунд."""
        buf = b""
        start = time.time()
        last = time.time()
        while time.time() - start < timeout:
            r, _, _ = select.select([self.master], [], [], 0.1)
            if r:
                try:
                    chunk = os.read(self.master, 65536)
                except OSError:
                    break
                if not chunk:
                    break
                buf += chunk
                last = time.time()
            elif time.time() - last >= idle:
                break
        return ANSI.sub("", buf.decode("utf-8", "replace")).replace("\r\n", "\n").replace("\r", "")

    def send(self, line, prefix=True):
        """Надсилає рядок у сеанс; у відповідь — ехо команди та її результат."""
        os.write(self.master, (line + "\n").encode())
        time.sleep(0.05)
        return ("sqlite> " if prefix else "") + self.read_idle()

    def send_block(self, lines):
        """Багаторядкова команда: перший рядок з запрошенням, решта — з «...>»."""
        return "".join(self.send(ln, prefix=(i == 0))
                       for i, ln in enumerate(lines))

    def close(self):
        """Коректно завершує сеанс sqlite3 і звільняє pty."""
        try:
            os.write(self.master, b".quit\n")
        except OSError:
            pass
        try:
            os.close(self.master)
        except OSError:
            pass
        deadline = time.time() + 3.0
        while time.time() < deadline:
            try:
                pid, _ = os.waitpid(self.pid, os.WNOHANG)
            except ChildProcessError:
                return
            if pid:
                return
            time.sleep(0.05)
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.kill(self.pid, sig)
                os.waitpid(self.pid, 0)
                return
            except (ProcessLookupError, ChildProcessError):
                return


def run(dbfile, cwd, steps, prompt_line=None):
    """steps: список (ім'я_кроку, [команди...]). Повертає {ім'я: транскрипт}."""
    out = {}
    s = SqliteSession(dbfile, cwd)
    banner = s.read_idle(idle=0.8)
    if prompt_line:
        out[prompt_line[0]] = prompt_line[1] + "\n" + banner.rstrip("\n ")
    for name, cmds in steps:
        text = ""
        for c in cmds:
            text += s.send_block(c) if isinstance(c, (list, tuple)) else s.send(c)
        out[name] = re.sub(r"(sqlite> ){2,}", "sqlite> ", text).rstrip("\n ")
        print("[ok] %-14s %s" % (name, str(cmds[0])[:60]))
    s.close()
    return out


def save(prefix, transcripts):
    os.makedirs(LOGS, exist_ok=True)
    for name, text in transcripts.items():
        path = os.path.join(LOGS, "%s_%s.txt" % (prefix, name))
        with open(path, "w") as f:
            f.write(text + "\n")
