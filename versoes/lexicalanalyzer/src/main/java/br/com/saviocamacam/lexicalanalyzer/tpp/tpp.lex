package br.com.saviocamacam.lexicalanalyzer.tpp;

import java_cup.runtime.*;

%%

%{


private TppToken createToken(String name, String value) {
    return new TppToken( name, value, yyline, yycolumn);
}

%}

%public
%class LexicalAnalyzer
%type TppToken
%line
%column

DIGITO = [0-9]
ACENTUACAO = �������������
INTEIRO = ([-+]?{DIGITO}+)
LETRA = [a-zA-Z]+
PR = (se|ent�o|sen�o|fim|repita|flutuante|retorna|at�|leia|escreve|inteiro)
CT = [{]+[\x20-\x7F�������������]+[}]+
ID = ([a-zA-Z�������������]([a-zA-Z�������������]*|[0-9]+)*)
FLUTUANTE = ({INTEIRO}"."{INTEIRO})
BRANCO = [\n| |\t|\r]+
SB = (:=|:|>|\{|\}|\(|\)|\*|=|-|<=|\[|\])
NUMBER_SN = ((\b[0-9]+)?\.)?\b[0-9]+([eE][-+]?[0-9]+)?\b

%%
{NUMBER_SN} {return createToken("SN", yytext()); }
{CT} { /**/ }
{PR} { return createToken("PR", yytext()); }
{INTEIRO} { return createToken("NUM", yytext()); }
{ID} { return createToken("ID", yytext()); }
{SB} { return createToken("SB", yytext()); }
{BRANCO} { /**/ }
{FLUTUANTE} {return createToken("NUM", yytext()); }


. { throw new RuntimeException("Caractere inv�lido " + yytext() + " na linha " + yyline + ", coluna " +yycolumn); }