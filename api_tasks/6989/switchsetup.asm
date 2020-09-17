p
u
s
h
 
e
b
p
 
.
 
m
o
v
 
e
b
p
,
 
e
s
p
 
.
 
a
n
d
 
e
s
p
,
 
v
a
r
 
.
 
s
u
b
 
e
s
p
,
 
v
a
r
 
.
 
p
u
s
h
 
e
b
x
 
.
 
p
u
s
h
 
e
s
i
 
.
 
p
u
s
h
 
e
d
i
 
.
 
c
a
l
l
 
v
a
r
 
.
 
x
o
r
 
e
b
x
,
 
e
b
x
 
.
 
c
m
p
 
e
a
x
,
 
e
b
x
 
.
 
m
o
v
 
d
w
o
r
d
 
[
e
s
p
 
+
 
v
a
r
]
,
 
e
a
x
 
.
 
j
n
e
 
v
a
r
 
.
 
p
u
s
h
 
6
 
.
 
p
u
s
h
 
e
b
x
 
.
 
c
a
l
l
 
d
w
o
r
d
 
[
s
y
m
.
i
m
p
.
o
l
e
3
2
.
d
l
l
_
C
o
I
n
i
t
i
a
l
i
z
e
E
x
]
 
.
 
c
a
l
l
 
d
w
o
r
d
 
[
s
y
m
.
i
m
p
.
K
E
R
N
E
L
3
2
.
d
l
l
_
G
e
t
C
o
m
m
a
n
d
L
i
n
e
W
]
 
.
 
p
u
s
h
 
s
t
r
.
b
o
o
t
s
t
r
a
p
 
.
 
m
o
v
 
e
d
i
,
 
e
a
x
 
.
 
m
o
v
 
d
w
o
r
d
 
[
e
s
p
 
+
 
v
a
r
]
,
 
v
a
r
 
.
 
c
a
l
l
 
v
a
r
 
.
 
c
m
p
 
e
a
x
,
 
e
b
x
 
.
 
j
e
 
v
a
r
 
.
 
m
o
v
 
b
y
t
e
 
[
e
s
p
 
+
 
v
a
r
]
,
 
1
 
.
 
a
d
d
 
e
a
x
,
 
v
a
r
 
.
 
j
m
p
 
v
a
r
 
.
 
c
m
p
 
c
x
,
 
v
a
r
 
.
 
j
n
e
 
v
a
r
 
.
 
i
n
c
 
e
a
x
 
.
 
i
n
c
 
e
a
x
 
.
 
m
o
v
z
x
 
e
c
x
,
 
w
o
r
d
 
[
e
a
x
]
 
.
 
c
m
p
 
c
x
,
 
b
x
 
.
 
j
n
e
 
v
a
r
 
.
 
m
o
v
z
x
 
e
c
x
,
 
w
o
r
d
 
[
e
a
x
]
 
.
 
x
o
r
 
e
s
i
,
 
e
s
i
 
.
 
c
m
p
 
c
x
,
 
b
x
 
.
 
j
e
 
v
a
r
 
.
 
x
o
r
 
e
d
x
,
 
e
d
x
 
.
 
m
o
v
z
x
 
e
c
x
,
 
c
x
 
.
 
c
m
p
 
c
x
,
 
v
a
r
 
.
 
j
e
 
v
a
r
 
.
 
i
n
c
 
e
s
i
 
.
 
m
o
v
 
w
o
r
d
 
[
e
s
p
 
+
 
e
d
x
 
+
 
v
a
r
]
,
 
c
x
 
.
 
l
e
a
 
e
d
x
,
 
d
w
o
r
d
 
[
e
s
i
 
+
 
e
s
i
]
 
.
 
m
o
v
z
x
 
e
c
x
,
 
w
o
r
d
 
[
e
d
x
 
+
 
e
a
x
]
 
.
 
c
m
p
 
c
x
,
 
b
x
 
.
 
j
n
e
 
v
a
r
 
.
 
p
u
s
h
 
v
a
r
 
.
 
m
o
v
 
e
a
x
,
 
e
d
i
 
.
 
m
o
v
 
w
o
r
d
 
[
e
s
p
 
+
 
e
s
i
*
2
 
+
 
v
a
r
]
,
 
b
x
 
.
 
c
a
l
l
 
v
a
r
 
.
 
t
e
s
t
 
e
a
x
,
 
e
a
x
 
.
 
j
e
 
v
a
r
 
.
 
m
o
v
 
d
w
o
r
d
 
[
e
s
p
 
+
 
v
a
r
]
,
 
s
t
r
.
b
s
e
l
d
l
g
 
.
 
j
m
p
 
v
a
r
 
.
 
m
o
v
 
b
y
t
e
 
[
e
s
p
 
+
 
v
a
r
]
,
 
b
l
 
.
 
m
o
v
 
w
o
r
d
 
[
e
s
p
 
+
 
v
a
r
]
,
 
b
x
 
.
 
p
u
s
h
 
s
t
r
.
L
Q
U
I
E
T
 
.
 
m
o
v
 
e
a
x
,
 
e
d
i
 
.
 
c
a
l
l
 
v
a
r
 
.
 
t
e
s
t
 
e
a
x
,
 
e
a
x
 
.
 
j
e
 
v
a
r
 
.
 
p
u
s
h
 
v
a
r
 
.
 
p
u
s
h
 
v
a
r
 
.
 
c
a
l
l
 
d
w
o
r
d
 
[
s
y
m
.
i
m
p
.
K
E
R
N
E
L
3
2
.
d
l
l
_
S
e
t
E
n
v
i
r
o
n
m
e
n
t
V
a
r
i
a
b
l
e
W
]