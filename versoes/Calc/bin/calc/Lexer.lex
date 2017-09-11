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

LineTerminator = \r|\n|\r\n
InputCharacter = [^\r\n]
WhiteSpace    = {LineTerminator} | [ \t\f]

Digit          = [0-9]
Number         = {Digit} {Digit}*
Letter         = [a-zA-Z] 

%%

<YYINITIAL> { 
    {Number}        { return symbol(Sym.NUMBER, new Integer(Integer.parseInt(yytext()))); }

    "+"             { return symbol(Sym.PLUS); }    
    "-"             { return symbol(Sym.MINUS); }
    "*"             { return symbol(Sym.TIMES); }
    "/"             { return symbol(Sym.DIVIDED); }

    "("             { return symbol(Sym.LPAREN); }
    ")"             { return symbol(Sym.RPAREN); }

    ";"             { return symbol(Sym.SEMI); }

    {WhiteSpace} {}
}

<<EOF>>             { return symbol( Sym.EOF ); }

[^]                 { throw new Error("Illegal character <" + yytext() + ">");}