#!/bin/sh
if [ -d "CMakeFiles" ];then rm -rf CMakeFiles; fi
if [ -f "Makefile" ];then rm -f Makefile; fi
if [ -f "cmake_install.cmake" ];then rm -f cmake_install.cmake; fi
if [ -f "CMakeCache.txt" ];then rm -f CMakeCache.txt; fi
cmake -DCMAKE_TOOLCHAIN_FILE="armgcc.cmake" -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=debug  .
make -j 2>&1 | tee debug/build_log.txt
