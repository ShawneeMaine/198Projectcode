# Enter your code here.

# Enter your code here.

# Enter your code here.

# Enter your code here.

# Enter your code here.

# Enter your code here.

# Enter your code here.


while 1==1
set x=0
set y=scanclosest()
  set x2=random()*10
  set y2=random()*10
call godest(x2,y2)
while y==getid()
  set z=godest(x2,y2)
  if z==2
    set x2=random()*10
    set y2=random()*10
  endif
  set x=x+10
  call scansetangle(x)
  set y=scanclosest()
endwhile
set x1=getxpos(y)+50
set y1=getypos(y)+50
call godest(x1,y1)
call scansetdest(x1-50,y1-50)
call firetrack(y)
endwhile





