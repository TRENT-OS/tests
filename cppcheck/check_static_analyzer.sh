#!/bin/bash -ue

#-------------------------------------------------------------------------------
# Copyright (C) 2021, HENSOLDT Cyber GmbH
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script executes cppcheck for a previously built project.
#
# Since cppcheck uses the CMake generated compile commands file the project has
# to be built before. The compile commands file and the path to the SDK source
# folder of the build have to be passed to the script.
#
# Some 3rd party folders are ignored by cppcheck. Additionally some patterns are
# filtered from the cppcheck output to ignore some false-positive issues.
#
# If there is at least one cppcheck issue, the script will return an error code.
#-------------------------------------------------------------------------------

OUT_FILE="cppcheck_output.txt"
OUT_FILE_FILTERED="cppcheck_output.txt.filtered"

#-------------------------------------------------------------------------------
# Show usage information
#-------------------------------------------------------------------------------
ARGUMENT1=${1:---help}
ARGUMENT2=${2:-}

if [ "${ARGUMENT1}" = "--help" ] || \
    [ -z "${ARGUMENT2}" ]; then

    USAGE_INFO="Usage: $(basename $0) [--help] COMPILE_CMD_FILE SDK_PATH
    --help              Show usage information.
    COMPILE_CMD_FILE    Compile commands file generated by the CMake build.
    SDK_PATH            Folder containing the SDK source code of the build."

    echo "${USAGE_INFO}"
    exit 0

fi

echo "---"
echo "Execute $(basename $0) in:"
echo $(pwd)
echo "-"

#-------------------------------------------------------------------------------
# Execute cppcheck.
#-------------------------------------------------------------------------------
COMPILE_CMD_FILE=$ARGUMENT1
SDK_PATH="$(realpath ${ARGUMENT2})"

cppcheck --project=${COMPILE_CMD_FILE} \
    --inline-suppr \
    --output-file=${OUT_FILE} \
    -i${SDK_PATH}/libs/3rdParty \
    -i${SDK_PATH}/libs/os_filesystem/3rdParty \
    -i${SDK_PATH}/libs/os_network_stack/3rdParty \
    -i${SDK_PATH}/sdk-sel4-camkes

# Workaround to append line break.
echo >> ${OUT_FILE}

# Remove empty lines.
sed -i '/^$/d' ${OUT_FILE}

echo "-"

# Log cppcheck output.
echo "Output of cppcheck:"
echo
cat ${OUT_FILE}
echo "-"

#-------------------------------------------------------------------------------
# Filter cppcheck output to ignore false-positive problems:
# - "#error" appears for preprocessor errors that are created due to a missing
#   configuration of libraries that are not used by the system.
#-------------------------------------------------------------------------------
EXCLUDE_PATTERNS=(
    \#error
)

grep -v ${EXCLUDE_PATTERNS[@]/#/-e} ${OUT_FILE} > ${OUT_FILE_FILTERED} || true

# Log filtered cppcheck output.
echo "Filtered output of cppcheck:"
echo
cat ${OUT_FILE_FILTERED}
echo "-"

#-------------------------------------------------------------------------------
# Check filtered output to detect cppcheck issues.
#-------------------------------------------------------------------------------
if [[ $(wc -l < ${OUT_FILE_FILTERED}) -gt 0 ]]; then

    echo "ERROR: cppcheck issues found."
    echo "---"

    exit 1 # error

fi

echo "INFO: No cppcheck issue found."
echo "---"

exit 0 # success