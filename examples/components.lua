function hello(a, b, c)
	d = a + b + c
	if d > 5 then
		return d
	elseif d > 10 then
		return d + 5
	else
		return 5
	end
end
hello, hello2 = hello(1,2,3), hello(2,3,4)
print(hello)

table = {x=1, y=2, z=3}
