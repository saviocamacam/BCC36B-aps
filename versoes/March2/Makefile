all:
	java -jar jflex-1.6.1.jar Lexer.lex
	java -jar java-cup-11b.jar -locations -interface -parser Parser -xmlactions Parser.cup
	javac -cp java-cup-11b-runtime.jar:. *.java
	java -cp java-cup-11b-runtime.jar:. Parser sintatica/teste-2.tpp simple.xml /

clean:
	rm -f Parser.java Lexer.java
	rm -f *.class