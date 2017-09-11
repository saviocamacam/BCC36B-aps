LEX := $(patsubst %.l,%.c,$(wildcard *.l))
YACC := $(patsubst %.y,%.tab.c,$(wildcard *.y))

all : $(YACC) $(LEX) calculadora.exe

parser.tab.c : parser.y
	bison -d -t $^

scanner.c : scanner.l
	flex -d -T $^
	
calculadora.exe :
	gcc parser.tab.c lex.yy.c -o $@ -lfl
	
clean : 
	rm -f $(LEX)
	rm -f *.yy.c
	rm *.exe
	rm *.tab.[ch]
