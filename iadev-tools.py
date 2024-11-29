#!/usr/bin/python3

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
import sys
import shutil
import urllib.request

def fetch_dev_tools():
  if os.path.isdir('./tools'):
    return
  try:
    print("\033[32mDownloading iadevtools...")
    urllib.request.urlretrieve("https://github.com/I-A-S/IADevTools/releases/download/release/iadevtools.zip", "./iadevtools.zip")
  except:
    print("\033[31mError while downloading iadevtools package.. Please try again in a bit.\033[39m")
    exit(-1)
  shutil.unpack_archive("./iadevtools.zip", './')
  os.remove('./iadevtools.zip')

def main(argc: int, argv: list[str]):
  fetch_dev_tools()
  from tools import iadev_tools
  iadev_tools.run(argc, argv)

if __name__ == "__main__":
  main(len(sys.argv), sys.argv)