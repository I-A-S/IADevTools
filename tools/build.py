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

import subprocess

from tools.util import log
from tools.util.iadev_config import IADevConfig
from tools.util.command_line import CommandLineBase

class BuildCommandLine(CommandLineBase):
  def __init__(self):
    super().__init__(BuildCommandLine.process_switch, BuildCommandLine.process_option)

    self.register_switch('debug', 'Build in debug mode')
    self.register_switch('release', 'Build in release mode')

    self.register_option('build-directory', 'Output directory for the build files')

    self.isDebug = False
    self.buildDirectory = './build'

  def process_switch(self, name: str):
    if name == 'debug':
      self.isDebug = True
    elif name == 'release':
      self.isDebug = False

  def process_option(self, name: str, value: str):
    if name == 'build-directory':
      self.buildDirectory = value

def generate(cmd: BuildCommandLine):
  def bool_to_cmake_opt_value(v):
    return 'ON' if v else 'OFF'

  if subprocess.run([
    'cmake',
    '-S', '.',
    '-B', f'./{cmd.buildDirectory}',
    '-G', 'Ninja',
    '-DCMAKE_C_COMPILER_LAUNCHER=ccache',
    '-DCMAKE_CXX_COMPILER_LAUNCHER=ccache',
    '-DCMAKE_C_COMPILER=clang-18',
    '-DCMAKE_CXX_COMPILER=clang++-18',
    f'-DIA_DEBUG_BUILD={bool_to_cmake_opt_value(cmd.isDebug)}'
  ]).returncode != 0:
    exit(-1)

def build(cmd: BuildCommandLine):
  if subprocess.run([
    'cmake',
    '--build',
    f'./{cmd.buildDirectory}'
  ]).returncode != 0:
    exit(-1)

def run(argc: int, argv: list[str]):
  IADevConfig.read_cached()
  cmd = BuildCommandLine()
  cmd.parse(argc, argv)
  generate(cmd)
  build(cmd)

if __name__ == "__main__":
  log.warn("Do not invoke this file directly, use `iadev-tools.py` from the root directory instead!")
  exit(-1)