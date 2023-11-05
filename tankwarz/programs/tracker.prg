# Enter your code here.

# Enter your code here.





# Enter your code here.

set x=30
call godest(x+maxx()/2,maxy()/2)

set ang=0
while 1==1
set gox=random()+maxx()/2
set goy=random()+maxy()/2
if godest(gox,goy)==2
  set gox=random()+maxx()/2
  set goy=random()+maxy()/2
endif
if scanclosest()!=getid()
 while scanclosest()!=getid()
   call scansetdest(getxpos(scanclosest()),getypos(scanclosest()))
   call firetarget(scanclosest()) 
   if godest(gox,goy)==2
     set gox=random()+maxx()/2
     set goy=random()+maxy()/2
#     set x=x*-1
   endif
 endwhile
endif
set ang=ang+getscanarc()
call scansetangle(ang)
endwhile


