number=0
resultado=0
while number<=1000 :
	if(number%3 == 0 or number%5 == 0):
		print(number)
		resultado+=number
	number+=1
print(resultado)