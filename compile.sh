make clean
make db_bench -j96 DEBUG_LEVEL=0 SPDK_DIR=../spdk EXTRA_CXXFLAGS="-Wno-deprecated-copy -Wno-pessimizing-move -Wno-error=stringop-truncation"
