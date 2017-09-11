{1. (Valor: 2.0 ). Dizemos que uma matriz quadrada inteira é um quadrado mágico se a soma dos elementos de cada linha, a soma dos elementos de cada coluna e a soma dos elementos das diagonais principal e secundária são todas iguais. Dada uma matriz quadrada A(nxn), verificar se A é um quadrado mágico.}

1.56966.58
inteiro principal()
	inteiro: A[tamanho_matriz][tamanho_matriz]
	inteiro: linha[tamanho_matriz]
	inteiro: coluna[tamanho_matriz]
	inteiro: diagonal_principal
	inteiro: diagonal_secundaria
	inteiro: i
	inteiro: j
	inteiro: contador
	inteiro: valor
	inteiro: somador
	inteiro: somador_temporario

	i := 0
	j := 0
	diagonal_principal := 0
	diagonal_secundaria := 0
	contador :=0
	valor := 0
	somador := 0

	repita
		repita
			leia(valor)
			A[i][j] = valor

			linha[i] = linha[i] + A[i][j]
			coluna[j] = coluna[j] + A[i][J]

			se i = j entao
				diagonal_principal = diagonal_principal + A[i][j]
			fim

			se (i + j + 1) = tamanho_matriz entao
				diagonal_secundaria = diagonal_secundaria + A[i][j]
			fim

		ate j < tamanho_matriz || x = 3
	ate i < tamanho_matriz

	repita
		se coluna[i] = linha[i] entao

		fim
	ate i < tamanho_matriz

	retorna(0)
fim