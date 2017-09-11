all:
	java -jar jflex-1.6.1.jar minijava.jflex
	java -jar java-cup-11b.jar -locations -interface -parser Parser -xmlactions minijava.cup
	javac -cp java-cup-11b-runtime.jar:. *.java
	java -cp java-cup-11b-runtime.jar:. Parser simple.minijava simple.xml /

clean:
	rm -f Parser.java Lexer.java
	rm -f *.class
