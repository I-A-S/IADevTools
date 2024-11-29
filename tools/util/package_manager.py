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
import urllib.error
import urllib.request

from tools.util import log
from tools.util import platform

PKG_REPO = "https://github.com/I-A-S/IAPackages/releases/download/release"

def install(name: str, on_status):
  os.makedirs("./packages/", exist_ok=True)
  install_aux(name, on_status)

def install_aux(name: str, on_status):
  pkg_config_path = f'./packages/{name}.iadpkg'
  if os.path.isfile(pkg_config_path): return
  pkg_file_name = f"{name}-{platform.name()}.zip"
  on_status(name)
  try:
    urllib.request.urlretrieve(f"{PKG_REPO}/{pkg_file_name}", f"./packages/{pkg_file_name}")
  except urllib.error.HTTPError:
    log.error(f"Couldn't find the package '{name}'.")
    exit(-1)
  except:
    log.error(f"Error while downloading the package {name}.. Please try again in a bit.")
    exit(-1)
  shutil.unpack_archive(f"./packages/{pkg_file_name}", './packages')
  os.remove(f"./packages/{pkg_file_name}")

  with open(pkg_config_path, 'r') as f:
    t = f.read().split(',')
    for i in range(int(t[2])):
      install_aux(t[3 + i], on_status)
