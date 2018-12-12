; ModuleID = "geracao/gencode-003.tpp"
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
  %"ret" = alloca i32, align 4
  store i32 25, i32* @"a"
  %"a" = load i32, i32* @"a"
  %"exp-test" = icmp sgt i32 %"a", 5
  br i1 %"exp-test", label %"if_true", label %"if_false"
exit-principal:
  %"retFin" = load i32, i32* %"retorno"
  ret i32 %"retFin"
if_true:
  %"a.1" = load i32, i32* @"a"
  %"exp-test.1" = icmp slt i32 %"a.1", 20
  br i1 %"exp-test.1", label %"if_true.1", label %"if_false.1"
if_false:
  store i32 0, i32* %"ret"
  br label %"if_end"
if_end:
  %"temp-" = load i32, i32* %"ret"
  store i32 %"temp-", i32* %"retorno"
  br label %"exit-principal"
if_true.1:
  store i32 1, i32* %"ret"
  br label %"if_end.1"
if_false.1:
  store i32 2, i32* %"ret"
  br label %"if_end.1"
if_end.1:
  br label %"if_end"
}
