from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import rmdir, rm, collect_libs
import os


required_conan_version = ">=2.0"


class VorbisConan(ConanFile):
    name = "vorbis"
    version = "1.3.7"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaConanBase"
    ignore_cpp_standard = True

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    requires = "ogg/1.3.5@aleya/public"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["INSTALL_CMAKE_PACKAGE_MODULE"] = False
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Vorbis")

        self.cpp_info.components["vorbis"].libs = ["vorbis"]
        self.cpp_info.components["vorbis"].set_property("cmake_target_name", "Vorbis::vorbis")

        if self.settings.os == "Linux":
            self.cpp_info.components["vorbis"].system_libs = ["m"]

        self.cpp_info.components["vorbisenc"].libs = ["vorbisenc"]
        self.cpp_info.components["vorbisenc"].set_property("cmake_target_name", "Vorbis::vorbisenc")
        self.cpp_info.components["vorbisenc"].requires = ["vorbis"]

        self.cpp_info.components["vorbisfile"].libs = ["vorbisfile"]
        self.cpp_info.components["vorbisfile"].set_property("cmake_target_name", "Vorbis::vorbisfile")
        self.cpp_info.components["vorbisfile"].requires = ["vorbis"]
