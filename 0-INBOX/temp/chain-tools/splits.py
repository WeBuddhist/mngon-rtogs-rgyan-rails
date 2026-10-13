import re,sys
tgt=open(sys.argv[1]).read(); res=open(sys.argv[2]).read()
HL=re.compile(r"^#{2,6} [^\n]*\^[\w-]+-0[ \t]*$",re.M)
# index of every non-ws char in target
pos=[i for i,c in enumerate(tgt) if not c.isspace()]
out=[]
for m in HL.finditer(res):
    n=len(re.sub(r"\s+","",HL.sub("",res[:m.start()])))
    if n==0: continue
    a=pos[n-1]+1; b=pos[n] if n<len(pos) else len(tgt)
    if "\n\n" not in tgt[a:b].replace(" ","").replace("\t",""):
        out.append((m.group(0).strip(), tgt[max(0,a-50):a]+" ⟦HERE⟧ "+tgt[b:b+50]))
print("split human blocks:",len(out))
for h,c in out[: int(sys.argv[3]) if len(sys.argv)>3 else 50]: print("-",h[:70],"\n   ",repr(c))
