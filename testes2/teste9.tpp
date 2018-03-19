
{ 1. (Valor: 2.0 ). Dizemos que uma matriz quadrada inteira ? um quadrado m?gico se a soma dos elementos de cada linha, a soma dos elementos de cada coluna e a soma dos elementos das diagonais principal e secund?ria s?o todas iguais. Dada uma matriz quadrada A(nxn), verificar se A ? um quadrado m?gico.}

{ (se)|(então)|(senão)|(fim)|(repita)|(flutuante)|(retorna)|(até)|(leia)|(escreva)|(inteiro)|(:=)|(:)|(>)|(<)|(\*)|(=)|(\-)|(\+)|(/)|(<=)|(>=)|(\[)|(\])|(')|(")|([a-zA-Zá-ñÁ-Ñ][a-zA-Zá-ñÁ-Ñ0-9_]*)|(\-?[0-9][0-9]*)|(\-?[0-9][0-9]*\.[0-9]+([Ee][-]?[0-9]+)?)|(\[^]*\)|(\n+)|( \t)|([])}

3-4
-4
-

inteiro principal(inteiro: tamanho_matriz)
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
	flutuante: var_teste

	i := 0
	j := 0
	diagonal_principal := 0
	diagonal_secundaria := 0
	contador :=0
	valor := 0
	somador := 0

	repita
		linha[i] := 0
		coluna[i] := 0
	até i < tamanho_matriz

	repita
		repita
			leia(valor)
			A[i][j] := valor

			linha[i] := linha[i] + A[i][j]
			coluna[j] := coluna[j] + A[i][j]

			se i = j então
				diagonal_principal := diagonal_principal + A[i][j]
			fim

			se (i + j + 1) = tamanho_matriz entao
				diagonal_secundaria := diagonal_secundaria + A[i][j]
			fim

		até j < tamanho_matriz
	até i < tamanho_matriz

	inteiro : resultado
	resultado := 1

	se diagonal_principal = diagonal_secundaria então
		i := 0
		resultado := 0
		repita
			se coluna[i] != linha[i] && linha[i] != diagonal_principal então
				resultado := 1
			fim
		até i < tamanho_matriz
	fim

	retorna(resultado)
fim