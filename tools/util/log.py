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

def status(msg: str):
  print(f"\033[32m🔹\033[3m {msg}\033[23;39m")

def info(msg: str):
  print(f"\033[1;34m💡 {msg}\033[22;39m")

def warn(msg: str):
  print(f"\033[1;33m🔸 {msg}\033[22;39m")

def error(msg: str):
  print(f"\033[1;31m🔸 {msg}\033[22;39m")
