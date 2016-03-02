cmake_minimum_required(VERSION 2.8.12)

project(OpenSonoGestures)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(OpenSonoGestures main.cpp)
add_executable(SplitClips splitclips.cpp)
target_link_libraries(OpenSonoGestures ${OpenCV_LIBS})
target_link_libraries(SplitClips ${OpenCV_LIBS})
