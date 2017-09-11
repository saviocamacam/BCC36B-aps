%{
  #include <stdio.h>

  int yyerror(char *);
  int yylex(void);
  int sym[26];
%}

%token INTEGER VARIABLE END_OF_FILE
%left '+' '-' 
%left '*' '/' 

%% 

program : 
			program statement '\n'
			|
			;

statement : 
			expr					{ printf("%d\n", $1); }
			| VARIABLE '=' expr		{ sym[$1] = $3; }
			;

expr : 
			INTEGER 
			| VARIABLE 				{ $$ = sym[$1]; }
			| expr '+' expr 		{ $$ = $1 + $3; }
			| expr '-' expr 		{ $$ = $1 - $3; }
			| expr '*' expr 		{ $$ = $1 * $3; }
			| expr '/' expr 		{ $$ = $1 / $3; }
			| '(' expr ')' 			{ $$ = $2; }
			;

%% 
int yyerror(char *s) {
	fprintf(stderr, "%s\n", s);
	return 0;
}

int main(void) {
	yyparse();
	return 0;
}
