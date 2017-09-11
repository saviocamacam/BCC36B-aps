inteiro principal()
	
	inteiro: valor
	inteiro: tamanho_vetor
	leia(tamanho_vetor)
	inteiro: vetor[tamanho_vetor]
	inteiro: somador
	somador := 0
	valor : = 0

	repita
		leia(valor)
		vetor[i] = valor

		i := i + 1
	ate i = tamanho_vetor

	leia(valor)

	repita
		se vetor[i] = valor
			somador := somador + 1
		fim

		i := i + 1
	ate i = tamanho_vetor


	retorna (somador)
fim