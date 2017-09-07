project(X3GWriter)
cmake_minimum_required(VERSION 3.2.3) #Only version it's tested with.

#Dependencies.
include(ExternalProject)
ExternalProject_Add(GPX
	GIT_REPOSITORY https://github.com/Ghostkeeper/GPX.git
	GIT_TAG feature_cmake
)
if(WIN32)
	find_program(GPX_EXECUTABLE gpx.exe PATHS "${CMAKE_INSTALL_PREFIX}/GPX/bin" "${CMAKE_INSTALL_PREFIX}/bin")
else()
	find_program(GPX_EXECUTABLE gpx PATHS "${CMAKE_INSTALL_PREFIX}/bin")
endif()
mark_as_advanced(GPX_EXECUTABLE)

#Installation.
set(installed_files
	__init__.py
	cfg.ini
	param.ini
	X3GWriter.py
	plugin.json
)
install(FILES ${installed_files} ${GPX_EXECUTABLE} DESTINATION .)