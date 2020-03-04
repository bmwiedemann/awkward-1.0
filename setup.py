# BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

import glob
import os
import platform
import subprocess
import sys
import distutils.util
import multiprocessing
import shutil

import setuptools
import setuptools.command.build_ext
import setuptools.command.install

from setuptools import setup, Extension

install_requires = open("requirements.txt").read().strip().split()

extras = {"test": open("requirements-test.txt").read().strip().split(),
          "docs": open("requirements-docs.txt").read().strip().split(),
          "dev":  open("requirements-dev.txt").read().strip().split()}
extras["all"] = sum(extras.values(), [])

tests_require = extras["test"]

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(setuptools.command.build_ext.build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " + ", ".join(x.name for x in self.extensions))

        for x in self.extensions:
            self.build_extension(x)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        cmake_args = ["-DCMAKE_INSTALL_PREFIX={0}".format(extdir),
                      "-DPYTHON_EXECUTABLE=" + sys.executable,
                      "-DPYBUILD=ON",
                      "-DCMAKE_OSX_DEPLOYMENT_TARGET=10.9",
                      "-DBUILD_TESTING=OFF"]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{0}={1}".format(cfg.upper(), extdir),
                           "-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE"]
            if sys.maxsize > 2**32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]

        if platform.system() == "Windows":
            build_args += ["/m"]
        else:
            build_args += ["-j", str(multiprocessing.cpu_count())]

        if not os.path.exists(self.build_temp):
             os.makedirs(self.build_temp)
        build_dir = self.build_temp

        # for scikit-build:
        # build_dir = os.path.join(DIR, "_pybuild")

        subprocess.check_call(["cmake", "-S", ext.sourcedir, "-B", build_dir] + cmake_args)
        subprocess.check_call(["cmake", "--build", build_dir] + build_args)
        subprocess.check_call(["cmake", "--build", build_dir, "--target", "install"])

if platform.system() == "Windows":
    # Libraries are not installed system-wide on Windows, but they do have to be in the awkward1 directory.
    libraries = []

    def tree(x):
        print(x + (" (dir)" if os.path.isdir(x) else ""))
        if os.path.isdir(x):
            for y in os.listdir(x):
                tree(os.path.join(x, y))

    class Install(setuptools.command.install.install):
        def run(self):
            print("----------------------------------------------------------------")
            tree("build")
            print("----------------------------------------------------------------")

            dlldir = os.path.join(os.path.join("build", "temp.%s-%d.%d" % (distutils.util.get_platform(), sys.version_info[0], sys.version_info[1])), "Release", "Release")
            tree(dlldir)
            print("----------------------------------------------------------------")
            for x in os.listdir(dlldir):
                if x.startswith("awkward"):
                    shutil.copyfile(os.path.join(dlldir, x), os.path.join(self.build_lib, "awkward1", x))
            print("----------------------------------------------------------------")
            setuptools.command.install.install.run(self)

else:
    # Libraries do not exist yet, so they cannot be determined with a glob pattern.
    libdir = os.path.join(os.path.join("build", "lib.%s-%d.%d" % (distutils.util.get_platform(), sys.version_info[0], sys.version_info[1])), "awkward1")
    static = ".a"
    if platform.system() == "Darwin":
        shared = ".dylib"
    else:
        shared = ".so"
    libraries = [("lib", [os.path.join(libdir, "libawkward-cpu-kernels-static" + static),
                          os.path.join(libdir, "libawkward-cpu-kernels" + shared),
                          os.path.join(libdir, "libawkward-static" + static),
                          os.path.join(libdir, "libawkward" + shared)])]

    Install = setuptools.command.install.install

setup(name = "awkward1",
      packages = setuptools.find_packages(where="src"),
      package_dir = {"": "src"},
      include_package_data = True,
      package_data = {"": ["*.dll"]},
      data_files = libraries + [
          ("include/awkward",             glob.glob("include/awkward/*.h")),
          ("include/awkward/cpu-kernels", glob.glob("include/awkward/cpu-kernels/*.h")),
          ("include/awkward/python",      glob.glob("include/awkward/python/*.h")),
          ("include/awkward/array",       glob.glob("include/awkward/array/*.h")),
          ("include/awkward/builder",     glob.glob("include/awkward/builder/*.h")),
          ("include/awkward/io",          glob.glob("include/awkward/io/*.h")),
          ("include/awkward/type",        glob.glob("include/awkward/type/*.h"))],
      version = open("VERSION_INFO").read().strip(),
      author = "Jim Pivarski",
      author_email = "pivarski@princeton.edu",
      maintainer = "Jim Pivarski",
      maintainer_email = "pivarski@princeton.edu",
      description = "Development of awkward 1.0, to replace scikit-hep/awkward-array in 2020.",
      long_description = "",
      long_description_content_type = "text/markdown",
      url = "https://github.com/jpivarski/awkward1",
      download_url = "https://github.com/jpivarski/awkward1/releases",
      license = "BSD 3-clause",
      entry_points = {
        "numba_extensions": ["init = awkward1._numba:register"]
      },
      test_suite = "tests",
      python_requires = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
      install_requires = install_requires,
      tests_require = extras["test"],
      extras_require = extras,

      # cmake_args=['-DBUILD_TESTING=OFF'],      # for scikit-build
      ext_modules = [CMakeExtension("awkward")], # NOT scikit-build
      cmdclass = {"build_ext": CMakeBuild,       # NOT scikit-build
                  "install": Install},

      classifiers = [
#         "Development Status :: 1 - Planning",
#         "Development Status :: 2 - Pre-Alpha",
#         "Development Status :: 3 - Alpha",
          "Development Status :: 4 - Beta",
#         "Development Status :: 5 - Production/Stable",
#         "Development Status :: 6 - Mature",
#         "Development Status :: 7 - Inactive",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: BSD License",
          "Operating System :: MacOS",
          "Operating System :: POSIX",
          "Operating System :: Unix",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Information Analysis",
          "Topic :: Scientific/Engineering :: Mathematics",
          "Topic :: Scientific/Engineering :: Physics",
          "Topic :: Software Development",
          "Topic :: Utilities",
          ])
