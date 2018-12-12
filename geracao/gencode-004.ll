; ModuleID = "geracao/gencode-004.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

@"n" = global i32 0, align 4
@"soma" = global i32 0, align 4
define i32 @"main"() 
{
entry-principal:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  store i32 10, i32* @"n"
  store i32 0, i32* @"soma"
  br label %"repita-loop"
exit-principal:
  %"retFin" = load i32, i32* %"retorno"
  ret i32 %"retFin"
repita-loop:
  %"left_side" = load i32, i32* @"soma"
  %"right_side" = load i32, i32* @"n"
  %"temp+" = add i32 %"left_side", %"right_side"
  store i32 %"temp+", i32* @"soma"
  %"left_side.1" = load i32, i32* @"n"
  %"temp-" = sub i32 %"left_side.1", 1
  store i32 %"temp-", i32* @"n"
  br label %"test-loop"
test-loop:
  %"n" = load i32, i32* @"n"
  %"exp-test" = icmp eq i32 %"n", 0
  br i1 %"exp-test", label %"repita-loop", label %"end"
end:
  %"writesoma" = load i32, i32* @"soma"
  call void @"escrevaInteiro"(i32 %"writesoma")
  store i32 0, i32* %"retorno"
  br label %"exit-principal"
}
