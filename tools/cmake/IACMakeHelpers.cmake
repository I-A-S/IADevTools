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

include(CheckIncludeFile)
include(CheckSymbolExists)
include(CheckStructHasMember)
include(CheckSourceCompiles)

set(IA_BUILT_DIR ${CMAKE_BINARY_DIR})
set(IA_INTERFACE_DIR ${IA_BUILT_DIR}/interface)
set(IA_GENERATED_DIR ${IA_BUILT_DIR}/generated)
set(IA_DUMMY_SRC_FILE ${IA_BUILT_DIR}/dummy.cpp)
if(NOT EXISTS ${IA_DUMMY_SRC_FILE})
  file(TOUCH ${IA_DUMMY_SRC_FILE})
endif()
file(MAKE_DIRECTORY ${IA_GENERATED_DIR} ${IA_INTERFACE_DIR})

if(IA_DEBUG_BUILD)
  add_compile_options("-g" "-Og")
  add_compile_definitions("-D__IA_DEBUG=1")
else()
  add_compile_options("-g0" "-Ofast")
  add_compile_definitions("-D__IA_DEBUG=0")
endif()

set(IA_TARGET_PLATFORM "Unknown")
set(IA_TARGET_PLATFORM_WIN OFF)
set(IA_TARGET_PLATFORM_MAC OFF)
set(IA_TARGET_PLATFORM_LINUX OFF)
if(WIN32)
  set(IA_TARGET_PLATFORM "win")
  set(IA_TARGET_PLATFORM_WIN ON)
elseif(CMAKE_SYSTEM_NAME MATCHES "Darwin")
  set(IA_TARGET_PLATFORM "mac")
  set(IA_TARGET_PLATFORM_MAC ON)
elseif(CMAKE_SYSTEM_NAME MATCHES "Linux")
  set(IA_TARGET_PLATFORM "linux")
  set(IA_TARGET_PLATFORM_LINUX ON)
endif()

# ------------------------------------------------------------
#                         MACROS
# ------------------------------------------------------------

macro(IA_INCLUDE_IF_EXISTS _path)
  if(EXISTS ${_path})
    include(${_path})
  endif()
endmacro()

macro(IA_PREFIX_AND_APPEND _list _prefix)
  set(TMP_PATHS ${ARGN})
  list(TRANSFORM TMP_PATHS PREPEND ${_prefix})
	list(APPEND ${_list} ${TMP_PATHS})
  unset(TMP_PATHS)
endmacro()

macro(IA_DECLARE_EXECUTABLE _name)
	add_executable(${_name} ${IA_DUMMY_SRC_FILE})
	set(IA_TARGET_SOURCES_${_name} "")
	set(IA_TARGET_HEADERS_${_name} "")
	set(IA_TARGET_CFLAGS_${_name} "")
	set(IA_TARGET_LDFLAGS_${_name} "")
	set(IA_TARGET_LIBS_${_name} "")
	set(IA_TARGET_DEPS_${_name} "")
	set(IA_TARGET_INCDIRS_${_name} "")
	set(IA_TARGET_LIBDIRS_${_name} "")

  IA_ADD_INCDIRS(${_name} ${CMAKE_SOURCE_DIR}/packages/inc/)
  IA_ADD_LIBDIRS(${_name} ${CMAKE_SOURCE_DIR}/packages/lib/)

  list(APPEND IA_TARGET_INCDIRS_${_name}
    ${IA_BUILT_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
  )
endmacro()

macro(IA_DECLARE_LIBRARY _name _type)
	add_library(${_name} ${_type} ${IA_DUMMY_SRC_FILE})

  set(${_name}_INTERFACE_HEADER_PATHS "")
  set(${_name}_INTERFACE_DIR ${IA_INTERFACE_DIR}/i${_name}/)
  set(${_name}_INTERFACE_DIR ${${_name}_INTERFACE_DIR} PARENT_SCOPE)
  file(MAKE_DIRECTORY ${${_name}_INTERFACE_DIR})

	set(IA_TARGET_SOURCES_${_name} "")
	set(IA_TARGET_HEADERS_${_name} "")
	set(IA_TARGET_CFLAGS_${_name} "")
	set(IA_TARGET_LDFLAGS_${_name} "")
	set(IA_TARGET_LIBS_${_name} "")
	set(IA_TARGET_DEPS_${_name} "")
	set(IA_TARGET_INCDIRS_${_name} "")
	set(IA_TARGET_LIBDIRS_${_name} "")
	set(IA_TARGET_EXPOSED_INCDIRS_${_name} "")
	set(IA_TARGET_INTERFACE_HEADERS_REL_${_name} "")
	set(IA_TARGET_INTERFACE_HEADERS_RFT_${_name} "")
	set(IA_TARGET_INTERFACE_HEADERS_ABS_${_name} "")
	set(IA_TARGET_INTERFACE_HEADER_DIRS_${_name} "")

  IA_ADD_INCDIRS(${_name} ${CMAKE_SOURCE_DIR}/packages/inc/)
  IA_ADD_LIBDIRS(${_name} ${CMAKE_SOURCE_DIR}/packages/lib/)

  list(APPEND IA_TARGET_INCDIRS_${_name}
    ${IA_BUILT_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
  )
endmacro()

macro(IA_ADD_SOURCES _name)
  IA_PREFIX_AND_APPEND(IA_TARGET_SOURCES_${_name} ${CMAKE_CURRENT_SOURCE_DIR}/ ${ARGN})
endmacro()

macro(IA_ADD_SOURCES_ABSOLUTE _name)
	list(APPEND IA_TARGET_SOURCES_${_name} ${ARGN})
endmacro()

macro(IA_ADD_HEADERS _name)
  IA_PREFIX_AND_APPEND(IA_TARGET_HEADERS_${_name} ${CMAKE_CURRENT_SOURCE_DIR}/ ${ARGN})
endmacro()

macro(IA_ADD_HEADERS_ABSOLUTE _name)
	list(APPEND IA_TARGET_HEADERS_${_name} ${ARGN})
endmacro()

macro(IA_ADD_CFLAGS _name)
	list(APPEND IA_TARGET_CFLAGS_${_name} ${ARGN})
endmacro()

macro(IA_ADD_LDFLAGS _name)
	list(APPEND IA_TARGET_LDFLAGS_${_name} ${ARGN})
endmacro()

macro(IA_ADD_LIBS _name)
	list(APPEND IA_TARGET_LIBS_${_name} ${ARGN})
endmacro()

macro(IA_ADD_DEPS _name)
	list(APPEND IA_TARGET_DEPS_${_name} ${ARGN})
endmacro()

macro(IA_ADD_INCDIRS _name)
	list(APPEND IA_TARGET_INCDIRS_${_name} ${ARGN})
endmacro()

macro(IA_ADD_LIBDIRS _name)
	list(APPEND IA_TARGET_LIBDIRS_${_name} ${ARGN})
endmacro()

macro(IA_ADD_EXPOSED_INCDIRS _name)
	list(APPEND IA_TARGET_EXPOSED_INCDIRS_${_name} ${ARGN})
endmacro()

macro(IA_ADD_INTERFACE_HEADERS _name)
	list(APPEND IA_TARGET_INTERFACE_HEADERS_REL_${_name} ${ARGN})
endmacro()
macro(IA_ADD_INTERFACE_HEADERS_FLAT _name)
	list(APPEND IA_TARGET_INTERFACE_HEADERS_RFT_${_name} ${ARGN})
endmacro()
macro(IA_ADD_INTERFACE_HEADERS_ABSOLUTE _name)
	list(APPEND IA_TARGET_INTERFACE_HEADERS_ABS_${_name} ${ARGN})
endmacro()
macro(IA_ADD_INTERFACE_HEADER_DIRS _name)
	list(APPEND IA_TARGET_INTERFACE_HEADER_DIRS_${_name} ${ARGN})
endmacro()
macro(IA_ADD_INTERFACE_HEADER_DIRS_FLAT _name)
  set(tmp "")
  foreach(_dir IN ITEMS ${ARGN})
    file(GLOB tmp CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${_dir}/*.h ${CMAKE_CURRENT_SOURCE_DIR}/${_dir}/*.hpp ${CMAKE_CURRENT_SOURCE_DIR}/${_dir}/*.inl)
    list(APPEND IA_TARGET_INTERFACE_HEADERS_ABS_${_name} ${tmp})
  endforeach()
  unset(tmp)
endmacro()

macro(IA_ADD_REFERENCES _name)
  foreach(ref IN ITEMS ${ARGN})
    IA_ADD_DEPS(${_name} ${ref})
    IA_ADD_LIBS(${_name} ${ref})
    IA_ADD_INCDIRS(${_name} ${${ref}_INTERFACE_DIR})
  endforeach()
endmacro()

macro(IA_ADD_PACKAGES _name)
  foreach(_package IN ITEMS ${ARGN})
    IA_ADD_LIBS(${_name} ${_package})
  endforeach()
endmacro()

macro(IA_DEFINE_EXECUTABLE _name)
  target_sources(${_name} PRIVATE ${IA_TARGET_SOURCES_${_name}})

  target_link_options(${_name} PUBLIC ${IA_TARGET_LDFLAGS_${_name}})
  target_link_libraries(${_name} PUBLIC ${IA_TARGET_LIBS_${_name}})
  target_compile_options(${_name} PUBLIC ${IA_TARGET_CFLAGS_${_name}})

  target_link_directories(${_name} PUBLIC ${IA_TARGET_LIBDIRS_${_name}})
  target_include_directories(${_name} PRIVATE ${IA_TARGET_INCDIRS_${_name}})

  list(LENGTH IA_TARGET_DEPS_${_name} dep_count)
  if(dep_count GREATER 0)
    add_dependencies(${_name} ${IA_TARGET_DEPS_${_name}})
  endif()
  list(LENGTH IA_TARGET_HEADERS_${_name} dep_count)
  if(dep_count GREATER 0)
    add_dependencies(${_name} ${IA_TARGET_HEADERS_${_name}})
  endif()
endmacro()

macro(IA_DEFINE_LIBRARY _name)
  IA_INCLUDE_IF_EXISTS(${CMAKE_CURRENT_SOURCE_DIR}/cmake/SourceFiles.cmake)
  
  target_sources(${_name} PRIVATE ${IA_TARGET_SOURCES_${_name}} ${IA_TARGET_HEADERS_${_name}})

  target_link_options(${_name} PUBLIC ${IA_TARGET_LDFLAGS_${_name}})
  target_link_libraries(${_name} PUBLIC ${IA_TARGET_LIBS_${_name}})
  target_compile_options(${_name} PUBLIC ${IA_TARGET_CFLAGS_${_name}})

  target_link_directories(${_name} PUBLIC ${IA_TARGET_LIBDIRS_${_name}})
  target_include_directories(${_name} PRIVATE ${IA_TARGET_INCDIRS_${_name}})
  target_include_directories(${_name} PUBLIC ${IA_TARGET_EXPOSED_INCDIRS_${_name}})
  
  list(LENGTH IA_TARGET_DEPS_${_name} dep_count)
  if(dep_count GREATER 0)
    add_dependencies(${_name} ${IA_TARGET_DEPS_${_name}})
  endif()

  foreach(hdr IN LISTS IA_TARGET_INTERFACE_HEADERS_REL_${_name})
    set(src "${CMAKE_CURRENT_SOURCE_DIR}/${hdr}")
    set(dst "${${_name}_INTERFACE_DIR}/${hdr}")
    add_custom_command(
      OUTPUT ${dst}
      COMMAND ${CMAKE_COMMAND} -E copy ${src} ${dst}
      DEPENDS ${src}
    )
    list(APPEND ${_name}_INTERFACE_HEADER_PATHS ${dst})
    unset(dst)
    unset(src)
  endforeach()
  foreach(hdr IN LISTS IA_TARGET_INTERFACE_HEADERS_RFT_${_name})
    cmake_path(GET hdr FILENAME srcName)
    set(src "${CMAKE_CURRENT_SOURCE_DIR}/${hdr}")
    set(dst "${${_name}_INTERFACE_DIR}/${_name}/${srcName}")
    add_custom_command(
      OUTPUT ${dst}
      COMMAND ${CMAKE_COMMAND} -E copy ${src} ${dst}
      DEPENDS ${src}
    )
    list(APPEND ${_name}_INTERFACE_HEADER_PATHS ${dst})
    unset(dst)
    unset(src)
  endforeach()
  foreach(hdr IN LISTS IA_TARGET_INTERFACE_HEADERS_ABS_${_name})
    cmake_path(GET hdr FILENAME srcName)
    set(dst "${${_name}_INTERFACE_DIR}/${_name}/${srcName}")
    add_custom_command(
      OUTPUT ${dst}
      COMMAND ${CMAKE_COMMAND} -E copy ${hdr} ${dst}
      DEPENDS ${hdr}
    )
    list(APPEND ${_name}_INTERFACE_HEADER_PATHS ${dst})
    unset(dst)
  endforeach()
  foreach(dir IN LISTS IA_TARGET_INTERFACE_HEADER_DIRS_${_name})
    set(dst_files "")
    set(src "${CMAKE_CURRENT_SOURCE_DIR}/${dir}")
    set(dst "${${_name}_INTERFACE_DIR}")
    file(GLOB_RECURSE src_files CONFIGURE_DEPENDS ${src}/*.h ${src}/*.hpp ${src}/*.inl)
    foreach(fileName IN LISTS src_files)
      string(REPLACE ${src} ${dst} tmp ${fileName})
      list(APPEND dst_files ${tmp})
    endforeach()
    add_custom_command(
      OUTPUT ${dst_files}
      COMMAND ${CMAKE_COMMAND} -E copy_directory ${src} ${dst}
      DEPENDS ${src_files}
    )
    list(APPEND ${_name}_INTERFACE_HEADER_PATHS ${dst_files})
    unset(dst_files)
    unset(dst)
    unset(src)
  endforeach()
  add_custom_target(${_name}_INTERFACE DEPENDS ${${_name}_INTERFACE_HEADER_PATHS})
  add_dependencies(${_name} ${_name}_INTERFACE)
endmacro()

macro(IA_INCLUDE_PLATFORM_CONFIG _cmakeDIR)
  IA_INCLUDE_IF_EXISTS(${_cmakeDIR}/platform/${IA_TARGET_PLATFORM}.cmake)
endmacro()

# ------------------------------------------------------------
#                      CONFIG FILE
# ------------------------------------------------------------

set(IA_CONFIG_FILE_OPTIONS "")

macro(IA_CONFIG_FILE_CALCULATE_OPTION_NAME _out)
  set(${_out} "")
  foreach(param IN ITEMS ${ARGN})
    set(tmp "")

    # if the first character is a '_', remove it
    set(tmp_c "")
    string(SUBSTRING ${param} 0 1 tmp_c)
    if(${tmp_c} STREQUAL "_")
      string(SUBSTRING ${param} 1 -1 tmp_c)
      string(TOUPPER ${tmp_c} tmp)
    else()
      string(TOUPPER ${param} tmp)
    endif()
    unset(tmp_c)

    string(REPLACE "." "_" tmp ${tmp})
    string(REPLACE "/" "_" tmp ${tmp})
    string(APPEND ${_out} "_${tmp}")
    unset(tmp)
  endforeach()
  string(SUBSTRING ${${_out}} 1 -1 ${_out})
endmacro()

macro(IA_CONFIG_FILE_ADD _name _value)
  set(${_name} ${_value})
  list(APPEND IA_CONFIG_FILE_OPTIONS "${_name} ${_value}")
endmacro()

macro(IA_CONFIG_FILE_ADD_CHECK _type _name)
  IA_CONFIG_FILE_CALCULATE_OPTION_NAME(name ${_name})
  if(${_type} STREQUAL "INCLUDE")
    check_include_file(${_name} ${name}_CHECK_RESULT)
  elseif((${_type} STREQUAL "FUNCTION") OR (${_type} STREQUAL "SYMBOL"))
    check_symbol_exists(${_name} ${ARGN} ${name}_CHECK_RESULT)
    check_symbol_exists(${_name} ${ARGN} ${name}_CHECK_RESULT)
  elseif(${_type} STREQUAL "CAN_COMPILE")
    check_cxx_source_compiles(${_name} ${ARGN} ${name}_CHECK_RESULT)
  endif()
  if(NOT ${name}_CHECK_RESULT)
    set(${name}_CHECK_RESULT 0)
  endif()
  IA_CONFIG_FILE_ADD("HAVE_${name}" ${${name}_CHECK_RESULT})
  unset(${name}_CHECK_RESULT)
endmacro()

macro(IA_CONFIG_FILE_GENERATE)
  string(TOLOWER ${CMAKE_PROJECT_NAME} CONFIG_FILE_NAME)
  set(CONFIG_FILE_NAME "${CONFIG_FILE_NAME}-config.hpp")
  set(IA_CONFIG_FILE_CONTENTS "#pragma once\n\n/* AUTO GENERATED. DO NOT EDIT. */\n\n")
  foreach(opt IN LISTS IA_CONFIG_FILE_OPTIONS)
    string(APPEND IA_CONFIG_FILE_CONTENTS "#define ${opt}\n")
  endforeach()
  if(NOT EXISTS ${IA_BUILT_DIR}/${CONFIG_FILE_NAME})
    file(WRITE ${IA_BUILT_DIR}/${CONFIG_FILE_NAME} ${IA_CONFIG_FILE_CONTENTS})
  endif()
  include_directories(${IA_BUILT_DIR})
  add_definitions(-DHAVE_IACONFIG_HPP=1)
  unset(CONFIG_FILE_NAME)
endmacro()
