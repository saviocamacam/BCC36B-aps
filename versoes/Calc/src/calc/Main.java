package calc;

import java.io.FileNotFoundException;
import java.io.FileReader;

public class Main {

    public static void main(String[] args) throws FileNotFoundException {

        String fileName = "C:/Users/savio/git/compiladores-aps/Calc/src/calc/calc.l";  
        Lexer lexer = new Lexer(new FileReader(fileName));
        Parser parser = new Parser(lexer);
        //Symbol token;
        
		/*try {
			while ((token = parser.getScanner().next_token()) != null) {
			    System.out.println("<" + "" + ", " + token.value + ">");
			}
		} catch (Exception e1) {
			e1.printStackTrace();
		}*/
		
        
        
        try {
            parser.parse();
        }       
        catch (Exception e) {
            System.out.println("Falha geral.");
        }
    }
}