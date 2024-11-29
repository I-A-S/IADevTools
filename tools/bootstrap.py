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

import shutil

from tools.util import log
from tools.util.iadev_config import IADevConfig

def check_for_dependencies(config: IADevConfig):
  BASE_DEPENDENCIES = ['cmake', 'ninja', 'ccache', 'clang-18']
  deps = BASE_DEPENDENCIES + config.dependencies
  for dep in deps:
    print(f"\033[33m  - Checking for {dep}..", end='')
    if not shutil.which(dep):
      print(f"\033[31mFAILED. Please install {dep} and make sure it's in the system path!\033[39m")
      exit(-1)
    print("")
  print("")

def install_required_packages(config: IADevConfig):
  from tools.util import package_manager
  installed_new_packages = False
  def on_status(name: str):
    installed_new_packages
    print(f"\033[33m  - Installing package {name}..")
  for pkg in config.packages:
    package_manager.install(pkg, on_status)
  if installed_new_packages: print("")

def run(argc: int, argv: list[str]):
  config = IADevConfig.read()
  log.status(f"Setting up {config.name}...\n")
  check_for_dependencies(config)
  install_required_packages(config)
  config.write_cached()
  log.status(f"Successfully bootstrapped {config.name}\n")
  log.info("Run 'iadev-tools.py build' to start building the project!\n")

if __name__ == "__main__":
  log.warn("Do not invoke this file directly, use `iadev-tools.py` from the root directory instead!")
  exit(-1)