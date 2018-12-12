; ModuleID = "geracao/gencode-001.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

@"a" = global i32 0, align 4
define i32 @"main"() 
{
entry-principal:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"b" = alloca i32, align 4
  store i32 10, i32* @"a"
  %"right_side" = load i32, i32* @"a"
  store i32 %"right_side", i32* %"b"
  %"temp-" = load i32, i32* %"b"
  store i32 %"temp-", i32* %"retorno"
  br label %"exit-principal"
exit-principal:
  %"retFin" = load i32, i32* %"retorno"
  ret i32 %"retFin"
}
