from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import load, save
from conan.tools.scm import Git


class LibCloudSyncConan(ConanFile):
    name = "libcloudsync"
    url = "https://github.com/jothepro/libCloudSync"
    description = """A simple to use C++ interface to interact with cloud storage providers."""
    settings = "os", "compiler", "build_type", "arch"
    license = "AGPL-3.0-or-later"
    exports = "VERSION"
    exports_sources = "lib/*", "test/*", "cmake/*", "example/*", "it/*", "VERSION", "LICENSE", "CMakeLists.txt"
    author = "jothepro"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "fakeit/*:integration": "catch",
        "libcurl/*:with_ftp": False,
        "libcurl/*:with_imap": False,
        "libcurl/*:with_mqtt": False,
        "libcurl/*:with_pop3": False,
        "libcurl/*:with_rtsp": False,
        "libcurl/*:with_smb": False,
        "libcurl/*:with_smtp": False,
        "libcurl/*:with_tftp": False,
    }

    def set_version(self):
        try:
            git = Git(self)
            self.version = git.run("describe --tags")[1:]
            save(self, "VERSION", self.version)
        except:
            try:
                self.version = load(self, "VERSION")
            except:
                self.version = "0.0.0"

    def requirements(self):
        self.requires("nlohmann_json/3.10.4")
        self.requires("pugixml/1.14")
        self.requires("libcurl/7.80.0")
        self.requires("cxxopts/3.0.0", visible=False)
        self.requires("catch2/3.7.1", visible=False)
        self.requires("fakeit/2.5.0", visible=False)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            self.options["libcurl/*"].with_ssl = "schannel"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        if not self.conf.get("tools.build:skip_test", default=False):
            tc.variables["BUILD_TESTING"] = True
        else:
            tc.variables["BUILD_TESTING"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if not self.conf.get("tools.build:skip_test", default=False):
            cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_target_name", "CloudSync::CloudSync")
        self.cpp_info.set_property("cmake_file_name", "CloudSync")
        self.cpp_info.libs = ["CloudSync"]
