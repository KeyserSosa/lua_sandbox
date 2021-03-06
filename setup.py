#!/usr/bin/env python2.7

import os
import json
import platform

from setuptools import setup, find_packages, Extension

build_config = {}

BUILDCONF = os.environ.get('LUASANDBOX_BUILDCONF', 'build.conf')

if os.path.exists(BUILDCONF):
    with open(BUILDCONF) as f:
        build_config = json.loads(f.read())

LUA_LIB = build_config.get('lua_lib', 'lua5.2')
INCLUDE_DIRS = build_config.get('include_dirs', [])
LIBRARY_DIRS = build_config.get('library_dirs', [])
EXTRA_COMPILE_ARGS = build_config.get('extra_compile_args', [])
EXTRA_LINK_ARGS = build_config.get('extra_link_args', [])

if 'jit' in LUA_LIB and platform.system() == 'Darwin':
    EXTRA_LINK_ARGS += ["-pagezero_size 10000", "-image_base 100000000"]

_executor = Extension('lua_sandbox._executor',
                      define_macros=[('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                      libraries=[LUA_LIB, 'm'],
                      library_dirs=LIBRARY_DIRS,
                      include_dirs=['c'] + INCLUDE_DIRS,
                      sources=['c/_executormodule.c', 'c/_luaexecutor.c'],
                      extra_compile_args=['-std=c99'] + EXTRA_COMPILE_ARGS,
                      extra_link_args=EXTRA_LINK_ARGS,
                      )

setup(
    name='lua-sandbox',
    version='1.0',
    description='A library to run lua code inside of a sandbox from Python',
    author='David King',
    author_email='dking@ketralnis.com',
    #url='https://docs.python.org/extending/building',
    ext_modules=[_executor],
    packages=find_packages(),
    package_data={'lua_sandbox': ['lua_sandbox/lua_utils/*.lua']},
    zip_safe=False,
    include_package_data=True,
    install_requires=[
    ],
)
