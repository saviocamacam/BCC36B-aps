inteiro: a, b
flutuante: d, e

flutuante func(inteiro: a, flutuante: v)
    retorna(1)
fim

inteiro principal()
	inteiro: digitado
	inteiro: i
	i := 1
	repita
		flutuante: f
		inteiro: int
		flutuante: resultado
		f := i/2
		int := i/2
		resultado := f - int
		
		se  resultado > 0 então
			escreva (i)
		fim
		i := i+1
	até i <= digitado
	retorna(1)
fim

