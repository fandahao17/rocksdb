make clean
make db_bench -j32 DEBUG_LEVEL=0 SPDK_DIR=../three EXTRA_CXXFLAGS="-Wno-deprecated-copy -Wno-pessimizing-move -Wno-error=stringop-truncation"
