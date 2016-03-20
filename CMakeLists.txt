cmake_minimum_required(VERSION 2.8.12)

project(OpenSonoGestures)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(FeatureGestureFlowMag FeatureGestureFlowMag.cpp)
add_executable(SplitClips splitclips.cpp)
add_executable(MotionGraph motiongraph.cpp)
add_executable(CheckOpenCL checkcl.cpp)
target_link_libraries(FeatureGestureFlowMag ${OpenCV_LIBS})
target_link_libraries(SplitClips ${OpenCV_LIBS})
target_link_libraries(MotionGraph ${OpenCV_LIBS})
target_link_libraries(CheckOpenCL ${OpenCV_LIBS})
