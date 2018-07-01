/* Calculadora parte 3. */
%{
#include <stdlib.h>
#include "syntax-tree.h"
#include "parser.tab.h"
void yyerror(char *);
%}

%%

[a-z] 		{   /* variables */
  				yylval.sIndex = *yytext - 'a';
  				return VARIABLE;
			}

0 			{   /* integers */
  				yylval.iValue = atoi(yytext);
  				return INTEGER;
			}

[1-9][0-9]*	{   /* integers */
  				yylval.iValue = atoi(yytext);
  				return INTEGER;
			}

[-()<>=+*/;{}.] 	{ 	/* operators */
				return *yytext;
			}

">="		return GE;
"<="		return LE;
"=="		return EQ;
"!="		return NE;
"while"		return WHILE;
"if"		return IF;
"else"		return ELSE;
"print"		return PRINT;

[ \t\n]+	;		/* skip whitespace */

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