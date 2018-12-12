all:
	clang -emit-llvm -S io.c
	llc -march=x86-64 -filetype=obj io.ll -o io.o
	llvm-link gencode-010.ll io.ll -o gencode-010.bc
	clang gencode-010.bc -o gencode-010.exe
	./gencode-010.exe
 clean:
	rm *.ll *.o *.bc