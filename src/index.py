DATA=[
	["VIP",">500","Yes",">40k",1],
	["VIP",">500","No",">40k",1],
	["VIP",">500","No",">40k",1],
	["VIP",">500","No","<40k",1],
	["VIP",">500","Yes","<40k",1],
	["VIP",">500","Yes","<40k",1],
	["VIP","<500","Yes","<40k",0],
	["VIP","<500","Yes",">40k",0],
	["Normal",">500","Yes",">40k",0],
	["Normal",">500","Yes","<40k",0],
	["Normal","<500","Yes",">40k",0],
	["Normal",">500","Yes",">40k",0],
	["Normal",">500","No","<40k",0],
	["Normal","<500","No","<40k",0],
	["Normal",">500","No",">40k",1],
	["Normal","<500","No",">40k",1]
]



def preprocess(dt):
	o=[]
	for i,k in enumerate(dt):
		o+=[[(e if j==len(k)-1 else (0 if e==dt[0][j] else 1)) for j,e in enumerate(k)]]
	return o



def decision_tree(l,ig=[]):
	def _cnt_nodes(k):
		if ("id" not in list(k.keys())):
			return 0
		return sum([_cnt_nodes(e) for e in k["ch"]])+len(k["ch"])
	if (all([e[4]==1 for e in l])):
		return {"r":1}
	if (all([e[4]==0 for e in l])):
		return {"r":0}
	if (len(ig)==len(l[0])-1):
		print(l)
		raise RuntimeError
	b=sorted([(abs(sum([l[j][i]*2-1 for j in range(0,len(l))]))/len(l),i) for i in range(0,len(l[0])-1) if i not in ig],key=lambda e:e[0])
	o=None
	bnc=None
	for k in b:
		to={"id":k[1],"ch":[]}
		for s in [0,1]:
			ch=[e for e in l if e[k[1]]==s]
			to["ch"]+=[{**decision_tree(ch,ig=ig+[k[1]]),"v":k}]
		nc=_cnt_nodes(to)
		if (bnc==None or nc<bnc):
			bnc=nc
			o=to
	return o



def graph(l,_i=0):
	if ("id" in list(l.keys())):
		o=f"#{l['id']}:"
		for k in [0,1]:
			o+=f"\n{' '*_i}  {k} -> {graph(l['ch'][k],_i=_i+2)}"
	else:
		o=f"@{l['r']}"
	if (_i==0):
		print(o)
	else:
		return o



graph(decision_tree(preprocess(DATA)))
