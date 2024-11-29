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

class CommandLineBase:
  def __init__(self, cb_process_switch, cb_process_option):
    self.options = []
    self.switches = []
    self.process_switch = cb_process_switch
    self.process_option = cb_process_option

  def register_option(self, name: str, description: str):
    self.options.append((name, description))

  def register_switch(self, name: str, description: str):
    self.switches.append((name, description))

  def parse(self, argc: int, argv: list[str]):
    for i in range(1, argc):
      arg = argv[i]
      if arg.startswith('--'):
        t = arg.find('=')
        if t >= 2:
          k = arg[2:t]
          v = arg[t+1:]
          if len(self.options) <= 0:
            log.error(f"Unrecognized option `{k}`")
            return False
          is_valid = False
          for name, _ in self.options:
            if name == k:
              self.process_option(self, k, v)
              is_valid = True
              break
          if not is_valid:
            log.error(f"Unrecognized option `{k}`")
            return False
        else:
          v = arg[2:]
          if v == 'help':
            self.display_help()
          if len(self.switches) <= 0:
            log.error(f"Unrecognized switch `{v}`")
            return False
          is_valid = False
          for name, _ in self.switches:
            if name == v:
              self.process_switch(self, v)
              is_valid = True
          if not is_valid:
            log.error(f"Unrecognized switch `{v}`")
            return False
      elif arg == 'help':
        self.display_help()
      else:
        log.error(f"Unrecognized command line argument `{arg}`")
        return False
    return True

  def display_help(self):
    print("\033[35mIADevTools; Script-Based Dev Tools for All IA Open Source Projects\nCopyright (C) 2024 IAS (ias@iasoft.dev)\033[39m\n")
    if len(self.options):
      print("\033[32mAvailable Options:")
      for v in self.options:
        print(f"\033[33m  | '--{v[0]}' ({v[1]})")
      print("\033[39m")
    if len(self.switches):
      print("\033[32mAvailable Switches:")
      for v in self.switches:
        print(f"\033[33m  | '--{v[0]}' ({v[1]})")
      print("\033[39m")
    exit(1)
