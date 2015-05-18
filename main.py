import scanner

s = """list a = {1 , 2, 3}
var x=a.length()
if(x>2)
{ list b = a.filter(r->r>2)
 print b
}
"""

p = scanner.Scanner(s)
tokens = p.parseInput()
for t in tokens:
    t.print()