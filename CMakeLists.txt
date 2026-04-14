cmake_minimum_required(VERSION 3.15)
project(qBreakpad VERSION 0.4.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt5 REQUIRED COMPONENTS Core Network)

set(BREAKPAD_SRC ${CMAKE_CURRENT_SOURCE_DIR}/third_party/breakpad/src)

# ---- Handler source files ----
set(HANDLER_SOURCES
    handler/QBreakpadHandler.cpp
    handler/QBreakpadHttpUploader.cpp
)

# ---- Windows-specific breakpad sources ----
if(WIN32)
    list(APPEND HANDLER_SOURCES
        ${BREAKPAD_SRC}/client/windows/crash_generation/crash_generation_client.cc
        ${BREAKPAD_SRC}/client/windows/handler/exception_handler.cc
        ${BREAKPAD_SRC}/common/windows/guid_string.cc
    )
endif()

# ---- Linux-specific breakpad sources ----
if(UNIX AND NOT APPLE)
    enable_language(ASM)
    list(APPEND HANDLER_SOURCES
        ${BREAKPAD_SRC}/client/minidump_file_writer.cc
        ${BREAKPAD_SRC}/common/convert_UTF.cc
        ${BREAKPAD_SRC}/common/md5.cc
        ${BREAKPAD_SRC}/common/string_conversion.cc
        ${BREAKPAD_SRC}/client/linux/crash_generation/crash_generation_client.cc
        ${BREAKPAD_SRC}/client/linux/dump_writer_common/thread_info.cc
        ${BREAKPAD_SRC}/client/linux/dump_writer_common/ucontext_reader.cc
        ${BREAKPAD_SRC}/client/linux/handler/exception_handler.cc
        ${BREAKPAD_SRC}/client/linux/handler/minidump_descriptor.cc
        ${BREAKPAD_SRC}/client/linux/log/log.cc
        ${BREAKPAD_SRC}/client/linux/microdump_writer/microdump_writer.cc
        ${BREAKPAD_SRC}/client/linux/minidump_writer/linux_core_dumper.cc
        ${BREAKPAD_SRC}/client/linux/minidump_writer/linux_dumper.cc
        ${BREAKPAD_SRC}/client/linux/minidump_writer/linux_ptrace_dumper.cc
        ${BREAKPAD_SRC}/client/linux/minidump_writer/minidump_writer.cc
        ${BREAKPAD_SRC}/common/linux/breakpad_getcontext.S
        ${BREAKPAD_SRC}/common/linux/elfutils.cc
        ${BREAKPAD_SRC}/common/linux/file_id.cc
        ${BREAKPAD_SRC}/common/linux/guid_creator.cc
        ${BREAKPAD_SRC}/common/linux/linux_libc_support.cc
        ${BREAKPAD_SRC}/common/linux/memory_mapped_file.cc
        ${BREAKPAD_SRC}/common/linux/safe_readlink.cc
    )
endif()

add_library(qBreakpad STATIC ${HANDLER_SOURCES})

target_include_directories(qBreakpad
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/handler>
        $<INSTALL_INTERFACE:include/qBreakpad>
    PRIVATE
        ${BREAKPAD_SRC}
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# lss (Linux Syscall Support) needed on Linux
if(UNIX AND NOT APPLE)
    target_include_directories(qBreakpad PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/third_party
    )
endif()

target_compile_definitions(qBreakpad PRIVATE CALIPER)

# Breakpad Windows sources use wide-char APIs (wchar_t), so UNICODE mode is required
if(WIN32)
    target_compile_definitions(qBreakpad PRIVATE UNICODE _UNICODE)
endif()

target_link_libraries(qBreakpad PUBLIC Qt5::Core Qt5::Network)

# ---- Install ----
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

install(TARGETS qBreakpad
    EXPORT qBreakpadTargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(FILES
    handler/QBreakpadHandler.h
    handler/QBreakpadHttpUploader.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/qBreakpad
)
install(FILES
    handler/singletone/singleton.h
    handler/singletone/call_once.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/qBreakpad/singletone
)

install(EXPORT qBreakpadTargets
    FILE qBreakpadTargets.cmake
    NAMESPACE qBreakpad::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/qBreakpad
)

configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/qBreakpadConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/qBreakpadConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/qBreakpad
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/qBreakpadConfig.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/qBreakpad
)
