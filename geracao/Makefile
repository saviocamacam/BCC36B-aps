all:
	clang -emit-llvm -S io.c
	llc -march=x86-64 -filetype=obj io.ll -o io.o
	llvm-link gencode-005.ll io.ll -o gencode-005.bc
	clang gencode-005.bc -o gencode-005.o
	./gencode-005.o
 clean:
	rm *.ll *.o *.bc 