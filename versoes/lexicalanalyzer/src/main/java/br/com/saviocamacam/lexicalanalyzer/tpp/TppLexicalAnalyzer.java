package br.com.saviocamacam.lexicalanalyzer.tpp;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;

public class TppLexicalAnalyzer {

	public static void main(String[] args) throws IOException {
		String rootPath = Paths.get("").toAbsolutePath(). toString();
        String subPath = "/src/main/java/br/com/saviocamacam/lexicalanalyzer/tpp";

        String sourceCode = rootPath + subPath + "/program_2.tpp";

        LexicalAnalyzer lexical = new LexicalAnalyzer(new FileReader(sourceCode));

        TppToken token;
        
        while ((token = lexical.yylex()) != null) {
            System.out.println("<" + token.name + ", " + token.value + ">" /*"(" + token.line + " - " + token.column + ")"*/);
        }
	}

}
