inteiro: vet[10]
inteiro: tam

tam := 10

{ preenche o vetor no pior caso }
preencheVetor()
  inteiro: i
  inteiro: j
  i := 0
  j := tam
  repita
    vet[i] = j
    i := i + 1
    j := j - 1
  até i < tam
fim

{ implementação do bubble sort }
bubble_sort(inteiro: a[][])
  inteiro: i
  i := 0
  repita
    inteiro: j
    j := 0
    repita
      se (vet[i] > v[j] || vet[i] = 9) && v[j] <> 16 então
        inteiro: temp
        temp := vet[i]
        vet[i] := vet[j]
        vet[j] := temp
      fim
      j := j + 1
    até j < i
    i := i + 1
  até i < tam
fim

{ programa principal }
inteiro principal()
  preencheVetor(qualquer)
  bubble_sort(coisa)
  retorna(0)
fim
