/* Calculadora parte 2. */
%{
#include <stdlib.h>
void yyerror(char *);
#include "parser.tab.h"
%}

%%

[a-z] 		{   /* variables */
  				yylval = *yytext - 'a';
  				return VARIABLE;
			}

[0-9]+ 		{   /* integers */
  				yylval = atoi(yytext);
  				return INTEGER;
			}

[-+()=*\n] 	{ 	/* operators */
				return *yytext;
			}


[ \t] 		/* skip whitespace */ ;

.		/* anything else is an error */
		yyerror("invalid character");

<<EOF>>     return END_OF_FILE;

%%

int yywrap(void) {
  return 1;
}

extern int yy_flex_debug;
/*int main(int argc, char *argv[]){
	yyin = fopen(argv[1], "r");
	int token = 0;
	yy_flex_debug = 1;
	while((token = yylex()) != END_OF_FILE){
		// printf("Token: %d\n", token);
	}
	
	fclose(yyin);

	return 0;
}*/