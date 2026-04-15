import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy


class QBreakpadConan(ConanFile):
    name = "qbreakpad"
    version = "0.4.1"
    license = "LGPL-2.1"
    description = "Qt wrapper for Google Breakpad crash reporting (Windows/Linux)"
    topics = ("qt", "breakpad", "crash-reporting", "minidump")
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False]}
    default_options = {
        "fPIC": True,
        # Qt: only build what we need (Core + Network), skip heavy modules
        "qt/*:shared": True,
        "qt/*:widgets": True,
        "qt/*:gui": True,
        # "qt/*:opengl": "no",
        # "qt/*:with_openssl": False,
        # "qt/*:gui": False,
        # "qt/*:widgets": False,
        # "qt/*:qtbase": True,
        # "qt/*:qtdeclarative": False,
        # "qt/*:qttools": False,
        # "qt/*:qtsvg": False,
        # "qt/*:qtmultimedia": False,
        # "qt/*:qttranslations": False,
        # "qt/*:qtdoc": False,
        # "qt/*:qtsensors": False,
        # "qt/*:qtconnectivity": False,
        # "qt/*:qtwayland": False,
        # "qt/*:qtimageformats": False,
        # "qt/*:qtwebengine": False,
        # "qt/*:qtwebchannel": False,
        # "qt/*:qtwebsockets": False,
        # "qt/*:qt3d": False,
        # "qt/*:qtlocation": False,
        # "qt/*:qtgamepad": False,
        # "qt/*:qtpurchasing": False,
        # "qt/*:qtscript": False,
        # "qt/*:qtxmlpatterns": False,
    }

    requires = "qt/5.15.18"

    # Export all sources needed to build the library
    exports_sources = (
        "CMakeLists.txt",
        "cmake/*",
        "handler/*",
        "third_party/breakpad/*",
        "third_party/lss/*",
    )

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        CMakeDeps(self).generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["qBreakpad"]
        self.cpp_info.includedirs = ["include/qBreakpad"]
        self.cpp_info.requires = ["qt::qtCore", "qt::qtNetwork"]
        self.cpp_info.set_property("cmake_target_name", "qBreakpad::qBreakpad")
        self.cpp_info.set_property("cmake_file_name", "qBreakpad")
