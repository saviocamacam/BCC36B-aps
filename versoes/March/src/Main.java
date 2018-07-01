import java.io.FileNotFoundException;
import java.io.FileReader;
import java.nio.file.Paths;


public class Main {

	public static void main(String[] args) {
		String rootPath = Paths.get("").toAbsolutePath(). toString();
		 String subPath = "/src/";
		 
		 String nameFile = args[0];
		 String sourceCode = rootPath + subPath + nameFile;
		 
		 Parser parser;
		try {
			parser = new Parser(new Lexer(new FileReader(sourceCode)));
			parser.parse();
		} catch (FileNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		 catch (Exception e) {
			 System.out.println("Falha geral.");
		 }
	}
}
