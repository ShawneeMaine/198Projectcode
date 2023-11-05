# Enter your code here.

set current=0
set arc=45
set x=random()*10
set y=random()*10
while godest(x,y)!=2
	call scansetangle(current)
	while current<360
		set id=scanclosest()
		if id!=getid()
			call firetrack(id)
		else
			set current=current+arc
			call scansetangle(current)
		endif
	endwhile
	set current=0
endwhile








