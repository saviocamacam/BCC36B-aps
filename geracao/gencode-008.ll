; ModuleID = "geracao/gencode-008.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

@"A" = global i32 0, align 4
@"B" = global i32 0, align 4
define i32 @"principal"() 
{
entry-principal:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"a" = alloca i32, align 4
  %"i" = alloca i32, align 4
  store i32 0, i32* %"i"
  br label %"repita-loop"
exit-principal:
  %"retFin" = load i32, i32* %"retorno"
  ret i32 %"retFin"
repita-loop:
  %"readIa" = call i32 @"leiaInteiro"()
  store i32 %"readIa", i32* %"a"
  %"right_side" = load i32, i32* %"a"
  store i32 %"right_side", i32* @"A"
  %"left_side" = load i32, i32* %"i"
  %"temp+" = add i32 %"left_side", 1
  store i32 %"temp+", i32* %"i"
  br label %"test-loop"
test-loop:
  %"i.1" = load i32, i32* %"i"
  %"exp-test" = icmp eq i32 %"i.1", 1024
  br i1 %"exp-test", label %"repita-loop", label %"end"
end:
  br label %"repita-loop.1"
repita-loop.1:
  %"right_side.1" = load i32, i32* %"i"
  %"temp-" = sub i32 1023, %"right_side.1"
  %"right_side.2" = load i32, i32* @"A"
  store i32 %"right_side.2", i32* @"B"
  %"left_side.1" = load i32, i32* %"i"
  %"temp+.1" = add i32 %"left_side.1", 1
  store i32 %"temp+.1", i32* %"i"
  br label %"test-loop.1"
test-loop.1:
  %"i.2" = load i32, i32* %"i"
  %"exp-test.1" = icmp eq i32 %"i.2", 1024
  br i1 %"exp-test.1", label %"repita-loop.1", label %"end.1"
end.1:
  br label %"repita-loop.2"
repita-loop.2:
  %"writeB" = load i32, i32* @"B"
  call void @"escrevaInteiro"(i32 %"writeB")
  %"left_side.2" = load i32, i32* %"i"
  %"temp+.2" = add i32 %"left_side.2", 1
  store i32 %"temp+.2", i32* %"i"
  br label %"test-loop.2"
test-loop.2:
  %"i.3" = load i32, i32* %"i"
  %"exp-test.2" = icmp eq i32 %"i.3", 1024
  br i1 %"exp-test.2", label %"repita-loop.2", label %"end.2"
end.2:
  store i32 0, i32* %"retorno"
  br label %"exit-principal"
}
