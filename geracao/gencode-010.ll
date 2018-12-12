; ModuleID = "geracao/gencode-010.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

@"n" = global i32 0, align 4
define i32 @"fatorial"(i32* %"n", i32* %"bla") 
{
entry-fatorial:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"fat" = alloca i32, align 4
  %"n.1" = load i32, i32* %"n"
  %"exp-test" = icmp sgt i32 %"n.1", 0
  br i1 %"exp-test", label %"if_true", label %"if_false"
exit-fatorial:
  %"retFin" = load i32, i32* %"retorno"
  ret i32 %"retFin"
if_true:
  store i32 1, i32* %"fat"
  br label %"repita-loop"
if_false:
  store i32 0, i32* %"retorno"
  br label %"if_end"
if_end:
  br label %"exit-fatorial"
repita-loop:
  %"left_side" = load i32, i32* %"fat"
  %"right_side" = load i32, i32* %"n"
  %"temp*" = mul i32 %"left_side", %"right_side"
  store i32 %"temp*", i32* %"fat"
  br label %"test-loop"
test-loop:
  %"n.2" = load i32, i32* %"n"
  %"exp-test.1" = icmp eq i32 %"n.2", 0
  br i1 %"exp-test.1", label %"repita-loop", label %"end"
end:
  %"temp-" = load i32, i32* %"fat"
  store i32 %"temp-", i32* %"retorno"
  br label %"if_end"
}

define i32 @"principal"() 
{
entry-principal:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"readIn" = call i32 @"leiaInteiro"()
  store i32 %"readIn", i32* @"n"
  %"retorno-fatorial" = call i32 @"fatorial"()
  call void @"escrevaInteiro"(i32 %"retorno-fatorial")
  store i32 0, i32* %"retorno"
  br label %"exit-principal"
exit-principal:
  %"retFin" = load i32, i32* %"retorno"
  ret i32 %"retFin"
}
