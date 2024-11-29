## IADevTools; Script-Based Dev Tools for All IA Open Source Projects 
## Copyright (C) 2024 IAS (ias@iasoft.dev)
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.

from tools.util import log

from tools import build
from tools import package
from tools import bootstrap

def display_help():
  print("\033[35mIADevTools; Script-Based Dev Tools for All IA Open Source Projects\nCopyright (C) 2024 IAS (ias@iasoft.dev)\n")
  print("\033[32mAvailable Commands:")
  print("\033[33m  - Build   (builds the project, run 'iadev-tools.py build help' for more)")
  print("\033[33m  - Package (packages the project, run 'iadev-tools.py package help' for more)")
  print("\033[39m")
  exit(1)

def run(argc: int, argv: list[str]):
  if (argc > 1):
    if argv[1] == 'build':
      build.run(argc - 1, argv[:1] + argv[2:])
    elif argv[1] == 'package':
      package.run(argc - 1, argv[:1] + argv[2:])
    elif argv[1] == 'help':
      display_help()
    else:
      log.error(f"Unknown command '{argv[1]}'")
      log.warn(f"Run 'iadev-tools.py help' for a valid list of commands!")
      exit(-1)
    return
  bootstrap.run(argc, argv)

if __name__ == "__main__":
  log.warn("Do not invoke this file directly, use `iadev-tools.py` from the root directory instead!")
  exit(-1)