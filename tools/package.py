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

import os
import shutil

from tools import build

from tools.util import log
from tools.util.iadev_config import IADevConfig

def package(name: str):
  PACKAGE_DIR = 'pkg-build'
  build.run(3, ['package', f'--build-directory={PACKAGE_DIR}', '--release'])
  os.makedirs(f'{PACKAGE_DIR}/pkg/inc', exist_ok=True)
  os.makedirs(f'{PACKAGE_DIR}/pkg/lib', exist_ok=True)
  shutil.copytree(f'{PACKAGE_DIR}/interface/i{name}/', f'{PACKAGE_DIR}/pkg/inc/', dirs_exist_ok=True)
  shutil.copytree(f'{PACKAGE_DIR}/lib/', f'{PACKAGE_DIR}/pkg/lib/', dirs_exist_ok=True)
  if os.path.isfile(f'{PACKAGE_DIR}/{name}-config.hpp'): shutil.copy(f'{PACKAGE_DIR}/{name}-config.hpp', f'{PACKAGE_DIR}/pkg/inc/{name}')
  shutil.copy('./tools/cached', f'{PACKAGE_DIR}/pkg/{name}.iadpkg')
  os.makedirs(f'./pkg')
  shutil.make_archive(f'./pkg/{name}', 'zip', f'{PACKAGE_DIR}/pkg/', f'./')
  shutil.rmtree(PACKAGE_DIR)
  return True

def run(argc: int, argv: list[str]):
  cfg = IADevConfig.read_cached()
  package(cfg.name)

if __name__ == "__main__":
  log.warn("Do not invoke this file directly, use `iadev-tools.py` from the root directory instead!")
  exit(-1)