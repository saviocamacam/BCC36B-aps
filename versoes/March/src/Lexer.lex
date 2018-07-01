import java_cup.runtime.*;

%%

%class Lexer
%unicode
%cup
%line
%column

%{
    private Symbol symbol(int type) {
        return new Symbol(type, yyline, yycolumn);
    }
    private Symbol symbol(int type, Object value) {
        return new Symbol(type, yyline, yycolumn, value);
    }
%}

	DIGITO = [0-9]
	LETRA = [a-zA-ZÃÕÂÊÁÉÔÍÓÚÇãõáéíóúâêôûüç\_]
	ID = {LETRA}({LETRA}|{DIGITO})*
	NUMERO = [0-9]*\.?[0-9]+([eE][-+][0-9]+)?
	BRANCO = [\n| |\t|\r]+
	CT = \{[^}]*\}
	ERROR_CT = [{}]
	ERROR = .
		
%%

<YYINITIAL> {
		"se"		{ return symbol(Sym.SE); }
		"então"		{ return symbol(Sym.ENTAO); }
		"senão"		{ return symbol(Sym.SENAO); }
		"fim"		{ return symbol(Sym.FIM); }
		"repita"	{ return symbol(Sym.REPITA); }
		"flutuante"	{ return symbol(Sym.FLUTUANTE); }
		"retorna"	{ return symbol(Sym.RETORNA); }
		"até"		{ return symbol(Sym.ATE); }
		"leia"		{ return symbol(Sym.LEIA); }
		"escreva"	{ return symbol(Sym.ESCREVA); }
		"inteiro"	{ return symbol(Sym.INTEIRO); }
		
		":="		{ return symbol(Sym.ATRIBUICAO); }
		":"			{ return symbol(Sym.DOISPONTOS); }
		">"			{ return symbol(Sym.MAIORQ); }
		"<"			{ return symbol(Sym.MENORQ); }
		"("		{ return symbol(Sym.EPARENTESES); }
		")"		{ return symbol(Sym.DPARENTESES); }
		"*"		{ return symbol(Sym.MULTIPLICACAO); }
		"<>"		{ return symbol(Sym.DIFERENTE); }
		"="			{ return symbol(Sym.IGUAL); }
		"-"		{ return symbol(Sym.SUBTRACAO); }
		"+"		{ return symbol(Sym.ADICAO); }
		"/"		{ return symbol(Sym.DIVISAO); }
		"<="		{ return symbol(Sym.MENORIGUALQ); }
		">="		{ return symbol(Sym.MAIORIGUALQ); }
		"["		{ return symbol(Sym.ECOLCHETES); }
		"]"		{ return symbol(Sym.DCOLCHETES); }
		","			{ return symbol(Sym.VIRGULA); }
		
		{NUMERO}	{ return symbol(Sym.NUMERO, new Integer(Integer.parseInt(yytext()))); }
		{ID}		{ return symbol(Sym.ID, new String(yytext())); }
		{BRANCO}	{}
		{ERROR_CT}	{System.out.println("Erro com comentário" + " na linha " + yyline + ", coluna " +yycolumn); }
		{ERROR} 	{System.out.println("Caractere inválido " + yytext() + " na linha " + yyline + ", coluna " +yycolumn);}
		{CT}		{}
}

<<EOF>>             { return symbol( Sym.EOF ); }
[^]                 { throw new Error("Illegal character <" + yytext() + ">");}