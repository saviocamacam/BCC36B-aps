package br.com.saviocamacam.lexicalanalyzer.tpp;

import java.io.File;
import java.nio.file.Paths;

public class GeneratorTpp {

	public static void main(String[] args) {
		String rootPath = Paths.get("").toAbsolutePath(). toString();
        String subPath = "/src/main/java/br/com/saviocamacam/lexicalanalyzer/tpp/";

        String file = rootPath + subPath + "tpp.lex";

        File sourceCode = new File(file);

        jflex.Main.generate(sourceCode);
	}

}
