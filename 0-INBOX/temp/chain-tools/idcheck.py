import re,sys,collections
s=open(sys.argv[1]).read()
blocks=[b for b in re.split(r"\n\s*\n",s) if b.strip()]
ids=[re.search(r"\^([\w-]+)\s*$",b) for b in blocks]
c=collections.Counter(i.group(1) for i in ids if i)
print(sys.argv[1].split('/')[-1],"blocks",len(blocks),"with id",sum(1 for i in ids if i),"dupes",[k for k,v in c.items() if v>1])
