cmake_minimum_required(VERSION 3.29)
project(BreakPadTest VERSION 1.0.0 LANGUAGES CXX)


find_package(qBreakpad REQUIRED)

add_subdirectory(./duplicates)

# --------------------------------------------------------------------------
# clangd: keep compile_commands.json at source root
# --------------------------------------------------------------------------
add_custom_target(copy_compile_commands ALL
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${CMAKE_BINARY_DIR}/compile_commands.json
        ${CMAKE_SOURCE_DIR}/compile_commands.json
    COMMENT "Copying compile_commands.json to source root"
)
