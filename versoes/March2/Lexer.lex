// Technische Universitaet Muenchen 
// Fakultaet fuer Informatik 

import java_cup.runtime.Symbol;
import java_cup.runtime.ComplexSymbolFactory;
import java_cup.runtime.ComplexSymbolFactory.Location;

%%

%public
%class Lexer
%cup
%implements sym
%char
%line
%column

%{
    StringBuffer string = new StringBuffer();
    public Lexer(java.io.Reader in, ComplexSymbolFactory sf){
	this(in);
	symbolFactory = sf;
    }
    ComplexSymbolFactory symbolFactory;

  private Symbol symbol(String name, int sym) {
      return symbolFactory.newSymbol(name, sym, new Location(yyline+1,yycolumn+1,yychar), new Location(yyline+1,yycolumn+yylength(),yychar+yylength()));
  }
  
  private Symbol symbol(String name, int sym, Object val) {
      Location left = new Location(yyline+1,yycolumn+1,yychar);
      Location right= new Location(yyline+1,yycolumn+yylength(), yychar+yylength());
      return symbolFactory.newSymbol(name, sym, left, right,val);
  } 
  private Symbol symbol(String name, int sym, Object val,int buflength) {
      Location left = new Location(yyline+1,yycolumn+yylength()-buflength,yychar+yylength()-buflength);
      Location right= new Location(yyline+1,yycolumn+yylength(), yychar+yylength());
      return symbolFactory.newSymbol(name, sym, left, right,val);
  }       
  private void error(String message) {
    System.out.println("Error at line "+(yyline+1)+", column "+(yycolumn+1)+" : "+message);
  }
%} 

%eofval{
     return symbolFactory.newSymbol("EOF", EOF, new Location(yyline+1,yycolumn+1,yychar), new Location(yyline+1,yycolumn+1,yychar+1));
%eofval}
	
	DIGITO = [0-9]
	LETRA = [a-zA-ZÃÕÂÊÁÉÔÍÓÚÇãõáéíóúâêôûüç\_]
	ID = {LETRA}({LETRA}|{DIGITO})*
	IntLiteral = 0 | [1-9][0-9]*
	FloLiteral = [0-9]*\.?[0-9]+
	SciLiteral = {FloLiteral}([eE][-+][0-9]+)?
	new_line = \r|\n|\r\n;
	BRANCO = {new_line} | [ \t\f]
	CT = \{[^}]*\}
	ERROR_CT = [{}]
	ERROR = .

%state STRING

%%

<YYINITIAL>{
	/* keywords */
	"se"              	{ return symbol("se",SE); }
	"então"            	{ return symbol("então",ENTAO); }
	"senão"            	{ return symbol("senão",SENAO); }
	"fim"            	{ return symbol("fim",FIM); }
	"repita"           	{ return symbol("repita",REPITA); }
	"flutuante"         { return symbol("flutuante",FLUTUANTE ); }
	"retorna"           { return symbol("retorna",RETORNA); }
	"até"           	{ return symbol("até",ATE); }
	"leia"            	{ return symbol("leia",LEIA); }
	"escreva"           { return symbol("escreva",ESCREVA); }
	"inteiro"          	{ return symbol("inteiro",INTEIRO); }
		
	
	/* names */
	{ID}           		{ return symbol("ID",ID, yytext()); }
	
	/* literals */
	{IntLiteral} 		{ return symbol("Intconst",INTCONST, new Integer(Integer.parseInt(yytext()))); }
	
	{FloLiteral} 		{ return symbol("Floconst",FLOCONST, new Float(Float.parseFloat(yytext()))); }
	
	{SciLiteral} 		{ return symbol("Sciconst",SCICONST, new Float(Float.parseFloat(yytext()))); }
	
	/* separators */
	":="               	{ return symbol("atribuicao",ATRIBUICAO); }
	":"               	{ return symbol("doispontos",DOISPONTOS); }
	"("               	{ return symbol("lpar",EPARENTESES); }
	")"               	{ return symbol("dpar",DPARENTESES); }
	"+"               	{ return symbol("add",ADICAO,"ADD"  ); }
	"-"               	{ return symbol("sub",SUBTRACAO, "SUB"  ); }
	"*"               	{ return symbol("mul",MULTIPLICACAO, "MUL"  ); }
	"/"               	{ return symbol("div",DIVISAO, "DIV"  ); }
	"<="              	{ return symbol("leq",MENORIGUALQ,  "LEQ"  ); }
	">="             	{ return symbol("geq",MAIORIGUALQ,  "GEQ"  ); }
	"="					{ return symbol("eq",IGUAL,  "EQ"   ); }
	"<>"             	{ return symbol("neq",DIFERENTE,  "NEQ"  ); }
	"<"               	{ return symbol("less",MENORQ,  "LESS"   ); }
	">"               	{ return symbol("gt",MAIORQ,  "GT"   ); }
	"["               	{ return symbol("ecol",ECOLCHETES); }
	"]"               	{ return symbol("dcol",DCOLCHETES); }
	","               	{ return symbol("virgula",VIRGULA); }
	
	{BRANCO}     		{ /* ignore */ }
	{ERROR_CT}			{System.out.println("Erro com comentário" + " na linha " + yyline + ", coluna " +yycolumn); }
	{ERROR} 			{System.out.println("Caractere inválido " + yytext() + " na linha " + yyline + ", coluna " +yycolumn);}
	{CT}				{ /* ignore */ }

}


/* error fallback */
[^]              {  /* throw new Error("Illegal character <"+ yytext()+">");*/
		    error("Illegal character <"+ yytext()+">");
                  }