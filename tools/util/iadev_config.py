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
import json

from tools.util import log

CONFIG_PATH = './iadev.json'
CACHED_CONFIG_PATH = './tools/cached'

class IADevConfig:
  def __init__(self):
    self.name = ''
    self.version = 0
    self.packages = []
    self.dependencies = []

  def write_cached(self):
    with open(CACHED_CONFIG_PATH, 'w') as f:
      f.write(f'{self.name},')
      f.write(f'{str(self.version)},')
      f.write(f'{str(len(self.packages))},')
      for v in self.packages: f.write(f'{v},')
      f.write(f'{str(len(self.dependencies))},')
      for v in self.dependencies: f.write(f'{v},')

  def read_cached():
    if not os.path.isfile(CACHED_CONFIG_PATH):
      log.error(f"Couldn't find the cached configuration `{CACHED_CONFIG_PATH}`")
      log.warn("Please run the `iadev-tools.py` from the root directory.")
      exit(-1)
    cfg = IADevConfig()
    with open(CACHED_CONFIG_PATH, 'r') as f:
      t = f.read().split(',')
      cfg.name = t[0]
      cfg.version = int(t[1])
      p = 3 + int(t[2])
      for i in range(int(t[2])): cfg.packages.append(t[3 + i])
      for i in range(int(t[p])): cfg.dependencies.append(t[p + 1 + i])
    return cfg

  def read():
    def handle_invalid():
      log.error(f"Invalid iadev configuration in the file `{CONFIG_PATH}`")
      log.warn("Please reclone from the repository and bootstrap again.")
      exit(-1)

    def parse_version(v: str):
      t = v.split('.')
      return ((int(t[0]) & 0x3FF) << 22) | ((int(t[1]) & 0x3FF) << 12) | (int(t[2]) & 0xFFF)

    if not os.path.isfile(CONFIG_PATH):
      log.error(f"Couldn't find the iadev configuration file `{CONFIG_PATH}`")
      log.warn("Please reclone from the repository and bootstrap again.")
      exit(-1)

    cfg = IADevConfig()

    with open(CONFIG_PATH, 'r') as f:
      raw = json.loads(f.read())
      if ('name' not in raw) or ('version' not in raw) or ('packages' not in raw) or ('dependencies' not in raw):
        handle_invalid()
      if (type(raw['name']) is not str) or (type(raw['version']) is not str) or (type(raw['packages']) is not list) or (type(raw['dependencies']) is not list):
        handle_invalid()
      for v in raw['packages']:
        if type(v) is not str: handle_invalid()
      for v in raw['dependencies']:
        if type(v) is not str: handle_invalid()
      cfg.name = raw['name']
      cfg.version = parse_version(raw['version'])
      cfg.packages = raw['packages']
      cfg.dependencies = raw['dependencies']

    return cfg
    