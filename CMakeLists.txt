project(X3GWriter)
cmake_minimum_required(VERSION 3.2.3) #Oldest version it's been tested with.

#Project metadata.
set(X3GWRITER_PLUGIN_NAME X3GWriter CACHE STRING "The name of the plug-in in distribution.")
set(X3GWRITER_VERSION_MAJOR 1 CACHE STRING "The major version number.")
set(X3GWRITER_VERSION_MINOR 1 CACHE STRING "The minor version number.")
set(X3GWRITER_VERSION_PATCH 12 CACHE STRING "The patch version number.")
set(X3GWRITER_SUPPORTED_SDKS "5.0.0;6.0.0;7.0.0" CACHE STRING "List of supported Cura SDK versions.")
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/plugin.json.in" "${CMAKE_CURRENT_BINARY_DIR}/plugin.json")

#Dependencies.
include(ExternalProject)
ExternalProject_Add(GPX
	GIT_REPOSITORY https://github.com/Ghostkeeper/GPX.git
	GIT_TAG feature_cmake
	CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR} -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} -DCMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH} -G ${CMAKE_GENERATOR}
	INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR} #Install to the current binary dir so as to not modify the user's system just for this dependency.
)
if(WIN32)
	find_program(GPX_EXECUTABLE gpx.exe PATHS "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}" "${CMAKE_CURRENT_BINARY_DIR}/bin" "${CMAKE_INSTALL_PREFIX}/GPX/bin" "${CMAKE_INSTALL_PREFIX}/bin")
else()
	find_program(GPX_EXECUTABLE gpx PATHS "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}" "${CMAKE_CURRENT_BINARY_DIR}/bin" "${CMAKE_INSTALL_PREFIX}/bin")
endif()
mark_as_advanced(GPX_EXECUTABLE)

#Installation.
set(installed_files
	__init__.py
	X3GWriter.py
	README.md
	LICENSE
	icon.svg
)
set(installed_executables #Which have to be installed with execute permissions.
	${GPX_EXECUTABLE}
)
set(installed_paths "")
foreach(f IN LISTS installed_files)
	list(APPEND installed_paths ${CMAKE_CURRENT_SOURCE_DIR}/${f})
endforeach()
list(APPEND installed_paths ${CMAKE_CURRENT_BINARY_DIR}/plugin.json)

#Find out where to install this thing.
if(WIN32)
	set(cura_directory "$ENV{APPDATA}\\cura")
elseif(APPLE)
	set(cura_directory "$ENV{HOME}/Library/Application Support/cura")
else()
	set(cura_directory "$ENV{HOME}/.local/share/cura")
endif()
#Figure out the latest Cura release that's installed.
file(GLOB versions RELATIVE "${cura_directory}" "${cura_directory}/*")
set(latest_version 2.0)
foreach(version ${versions})
	if(IS_DIRECTORY "${cura_directory}/${version}")
		if(${version} VERSION_GREATER ${latest_version})
			set(latest_version ${version})
		endif()
	endif()
endforeach()
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
	set(CMAKE_INSTALL_PREFIX "${cura_directory}/${latest_version}/plugins" CACHE PATH "Location of the Cura plug-ins folder to install this plug-in to." FORCE)
endif()
install(FILES ${installed_paths} DESTINATION X3GWriter)
install(FILES ${installed_executables} DESTINATION X3GWriter PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)

#Packing this into a .curapackage file.
add_custom_target(pack COMMAND "") #Packs for all supported SDK versions.
foreach(sdk_version ${X3GWRITER_SUPPORTED_SDKS})
	file(COPY ${installed_paths} DESTINATION pack${sdk_version}/files/plugins/X3GWriter)
	file(COPY ${installed_executables} DESTINATION pack${sdk_version}/files/plugins/X3GWriter)
	file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/cmake/[Content_Types].xml" DESTINATION pack${sdk_version})
	file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/cmake/_rels" DESTINATION pack${sdk_version})
	configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/package.json.in" pack${sdk_version}/package.json)
	set(packaged_files
		package.json
		[Content_Types].xml
		_rels
		files
	)
	add_custom_target(pack${sdk_version}
		COMMAND "${CMAKE_COMMAND}" -E tar cfv ../X3GWriter${sdk_version}.curapackage --format=zip ${packaged_files}
		WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pack${sdk_version}
	)
	add_dependencies(pack pack${sdk_version})
endforeach()

#Let CPack find it.
include(InstallRequiredSystemLibraries)
set(CPACK_PACKAGE_VERSION_MAJOR ${X3GWRITER_VERSION_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR ${X3GWRITER_VERSION_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH ${X3GWRITER_VERSION_PATCH})
set(CPACK_PACKAGE_NAME ${X3GWRITER_PLUGIN_NAME})
set(CPACK_PACKAGE_DESCRIPTION_FILE ${CMAKE_CURRENT_SOURCE_DIR}/README.md)
set(CPACK_GENERATOR ZIP)
include(CPack)
