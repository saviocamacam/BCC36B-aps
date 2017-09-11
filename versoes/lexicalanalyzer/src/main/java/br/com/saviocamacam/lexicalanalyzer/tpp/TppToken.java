package br.com.saviocamacam.lexicalanalyzer.tpp;

public class TppToken {
	
	public String name;
    public String value;
    public Integer line;
    public Integer column;

    public TppToken(String name, String value, Integer line, Integer column) {
        this.name = name;
        this.value = value;
        this.line = line;
        this.column = column;
    }

}
