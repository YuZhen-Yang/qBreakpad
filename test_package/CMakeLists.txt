cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(qBreakpad REQUIRED)
find_package(Qt5 REQUIRED COMPONENTS Core)

add_executable(test_package test_package.cpp)
target_link_libraries(test_package PRIVATE qBreakpad::qBreakpad Qt5::Core)
