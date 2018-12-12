; ModuleID = "geracao/savio.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

define i32 @"soma"(i32* %"a", i32* %"b") 
{
entry-soma:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"left_side" = load i32, i32* %"a"
  %"right_side" = load i32, i32* %"b"
  %"temp+" = add i32 %"left_side", %"right_side"
  store i32 %"temp+", i32* %"retorno"
  br label %"exit-soma"
exit-soma:
  %"retFin" = load i32, i32* %"retorno"
  ret i32 %"retFin"
}

define i32 @"principal"() 
{
entry-principal:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  store i32 2, i32* %"a"
  %"right_side" = load i32, i32* %"a"
  store i32 %"right_side", i32* %"b"
  store i32 0, i32* %"retorno"
  br label %"exit-principal"
exit-principal:
  %"retFin" = load i32, i32* %"retorno"
  ret i32 %"retFin"
}
