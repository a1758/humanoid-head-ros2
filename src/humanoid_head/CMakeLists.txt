cmake_minimum_required(VERSION 3.8)
project(humanoid_head)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

install(DIRECTORY
  urdf config launch worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  scripts/expression_engine
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
