cmake_minimum_required(VERSION 3.12.0)
project(yurlungur)

include_directories(include)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/pybind11/tools)
#https://cmake.org/cmake/help/git-stage/module/FindPython.html
#find_package(PythonExtensions REQUIRED)
find_package (Python COMPONENTS Interpreter Development)
add_library(_yurlungur MODULE src/_yurlungur.cpp)
#python_extension_module(_yurlungur)
install(TARGETS _yurlungur LIBRARY DESTINATION yurlungur)
