inteiro: n
inteiro fatorial(inteiro: n)
	inteiro: fat
	se n > 0 ent�o {n�o calcula se n > 0}
		fat := 1
		repita
			fat := fat * n
			n := n - 1
		at� n = 0
		retorna(fat) {retorna o valor do fatorial de n}
	sen�o
		retorna(0)
	fim
fim

inteiro principal()
	leia(n)
	escreva(fatorial(n))
	retorna(0)
fim