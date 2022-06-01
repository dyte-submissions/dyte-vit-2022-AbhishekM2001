from pandas import read_csv
from credentials import *
from github import Github
import base64
import sys
import pandas
g=Github("AbhishekM2001",passwd)

def get_version(x):
	r=g.get_repo(x)
	# print(r.name)
	contents=r.get_contents("package.json")
	# print(dir(contents))
	text=base64.b64decode(contents.content)
	v=text.index(b'version')
	i=v+10
	j=text.index(b'"',i+1)
	# print(text[i+1:j])
	return text[i+1:j].decode("utf-8")
# version=get_version("dyte-in/react-sample-app")
# print(version)

if __name__=='__main__':
	# print(get_version("dyte-in/react-sample-app"))
	# for i in range(len(sys.argv)):
	# 	print(i,sys.argv[i])
	
	if(sys.argv[1]=='-i'):
		df=read_csv(sys.argv[2])
		# print(df['repo'][1])
		v1=sys.argv[3][sys.argv[3].index('@')+1:]
	
	if(sys.argv[1]=='-update' and sys.argv[2]=='-i'):
		df=read_csv(sys.argv[3])
		v1=sys.argv[4][sys.argv[4].index('@')+1:]
		
	v=[]
	for i in range(len(df['repo'])):
		t=df['repo'][i].index('dyte-in')
		s=df['repo'][i][t:]
		v2=get_version(s.rstrip('/'))
		# print(v2)
		v.append(v2)
	df['version']=v
	comp=[]
	for i in range(len(v)):
		a1=v1.index('.')
		a2=v[i].index('.')
		b1=v1.index('.',a1+1)
		b2=v[i].index('.',a2+1)
		# print(a1,b1,a2,b2)
		# print(v1[:a1],v[i][:a2])
		if(int(v[i][:a2])>int(v1[:a1])):
			comp.append('true')
		elif(int(v[i][a2+1:b2])>int(v1[a1+1:b1])):
			comp.append('true')
		elif(int(v[i][b2+1:])>int(v1[b1+1:])):
			comp.append('true')
		else:
			comp.append('false')
	# print(comp)
	df['version_satisfied']=comp
	# print(df)

	if(sys.argv[1]=='-update' and sys.argv[2]=='-i'):
		
		for i in range(len(comp)):
			if(comp[i]=='false'):
				t=df['repo'][i].index('dyte-in')
				s=df['repo'][i][t:]
				rep=g.get_repo(s.rstrip('/'))
				pulls=rep.get_pulls(state='open')
				mx=-100
				for p in pulls:
					mx=p.number if mx>p.number else mx
				print(mx)




