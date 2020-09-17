c
a
l
l
 
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
 
i
n
t
 
.
 
i
n
t
 
.
 
i
n
t
 
.
 
i
n
t
 
.
 
i
n
t
 
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
b
p
 
-
 
v
a
r
]
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
b
p
 
-
 
4
]
,
 
e
b
x
 
.
 
l
e
a
 
e
a
x
,
 
d
w
o
r
d
 
[
e
b
p
 
-
 
v
a
r
]
 
.
 
p
u
s
h
 
e
a
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
S
t
a
r
t
u
p
I
n
f
o
A
]
 
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
b
p
 
-
 
4
]
,
 
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
b
p
 
-
 
4
]
,
 
1
 
.
 
m
o
v
 
e
a
x
,
 
d
w
o
r
d
 
f
s
:
[
v
a
r
]
 
.
 
m
o
v
 
e
d
i
,
 
d
w
o
r
d
 
[
e
a
x
 
+
 
4
]
 
.
 
m
o
v
 
e
s
i
,
 
e
b
x
 
.
 
m
o
v
 
e
d
x
,
 
v
a
r
 
.
 
:
 
v
a
r
 
8
b
c
f
 
m
o
v
 
e
c
x
,
 
e
d
i
 
.
 
:
 
v
a
r
 
3
3
c
0
 
x
o
r
 
e
a
x
,
 
e
a
x
 
.
 
:
 
v
a
r
 
f
0
0
f
b
1
0
a
 
l
o
c
k
 
c
m
p
x
c
h
g
 
d
w
o
r
d
 
[
e
d
x
]
,
 
e
c
x
 
.
 
:
 
v
a
r
 
8
5
c
0
 
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
 
|
:
 
v
a
r
 
3
b
c
7
 
c
m
p
 
e
a
x
,
 
e
d
i
 
.
 
j
n
e
 
v
a
r
 
.
 
|
|
:
 
v
a
r
 
3
3
f
6
 
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
 
|
|
:
 
v
a
r
 
4
6
 
i
n
c
 
e
s
i
 
.
 
c
m
p
 
d
w
o
r
d
 
[
v
a
r
]
,
 
1
 
.
 
j
n
e
 
v
a
r
 
.
 
|
|
:
 
v
a
r
 
6
a
1
f
 
p
u
s
h
 
v
a
r
 
.
 
|
|
:
 
v
a
r
 
e
8
3
4
0
4
0
0
0
0
 
c
a
l
l
 
v
a
r
 
.
 
|
|
:
 
v
a
r
 
5
9
 
p
o
p
 
e
c
x
 
.
 
j
m
p
 
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
 
|
:
 
v
a
r
 
f
f
1
5
4
c
d
0
4
0
0
0
 
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
l
e
e
p
]
 
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
 
d
w
o
r
d
 
[
v
a
r
]
,
 
e
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
 
d
w
o
r
d
 
[
v
a
r
]
,
 
1
 
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
 
v
a
r
 
.
 
p
o
p
 
e
c
x
 
.
 
p
o
p
 
e
c
x
 
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
 
d
w
o
r
d
 
[
v
a
r
]
,
 
1
 
.
 
c
m
p
 
d
w
o
r
d
 
[
v
a
r
]
,
 
1
 
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
 
v
a
r
 
.
 
p
o
p
 
e
c
x
 
.
 
p
o
p
 
e
c
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
v
a
r
]
,
 
2
 
.
 
t
e
s
t
 
e
s
i
,
 
e
s
i
 
.
 
j
n
e
 
v
a
r
 
.
 
x
o
r
 
e
a
x
,
 
e
a
x
 
.
 
m
o
v
 
e
c
x
,
 
v
a
r