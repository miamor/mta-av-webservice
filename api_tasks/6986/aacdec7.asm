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
 
"
S
V
W
h
"
 
.
 
a
d
c
 
b
y
t
e
 
[
e
a
x
]
,
 
a
l
 
.
 
p
u
s
h
 
s
t
r
.
S
o
f
t
w
a
r
e
_
_
M
i
c
r
o
s
o
f
t
_
_
W
i
n
d
o
w
s
_
_
C
u
r
r
e
n
t
V
e
r
s
i
o
n
 
.
 
m
o
v
 
e
s
i
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
s
i
 
.
 
l
e
a
 
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
b
p
 
-
 
v
a
r
]
 
.
 
c
a
l
l
 
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
 
p
u
s
h
 
e
a
x
 
.
 
l
e
a
 
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
b
p
 
-
 
v
a
r
]
 
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
u
s
h
 
s
t
r
.
w
t
 
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
 
p
u
s
h
 
e
a
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
 
m
o
v
 
b
y
t
e
 
[
e
b
p
 
-
 
1
]
,
 
0
 
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
d
i
,
 
e
d
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
 
2
 
.
 
p
u
s
h
 
e
d
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
 
p
u
s
h
 
v
a
r
 
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
C
r
e
a
t
e
F
i
l
e
A
]
 
.
 
c
m
p
 
e
a
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
C
l
o
s
e
H
a
n
d
l
e
]
 
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
D
e
l
e
t
e
F
i
l
e
A
]
 
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
 
s
t
r
.
s
h
e
l
l
3
2
.
d
l
l
 
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
b
p
 
-
 
v
a
r
]
,
 
0
 
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
b
p
 
-
 
1
]
,
 
1
 
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
L
o
a
d
L
i
b
r
a
r
y
A
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
S
H
G
e
t
F
o
l
d
e
r
P
a
t
h
A
 
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
P
r
o
c
A
d
d
r
e
s
s
]
 
.
 
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
e
 
v
a
r
 
.
 
l
e
a
 
e
c
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
 
"
Q
W
W
j
"
 
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
 
e
a
x
 
.
 
c
m
p
 
b
y
t
e
 
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
 
0
 
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
 
s
t
r
.
A
p
p
D
a
t
a
 
.
 
p
u
s
h
 
s
t
r
.
S
o
f
t
w
a
r
e
_
_
M
i
c
r
o
s
o
f
t
_
_
W
i
n
d
o
w
s
_
_
C
u
r
r
e
n
t
V
e
r
s
i
o
n
_
_
E
x
p
l
o
r
e
r
_
_
S
h
e
l
l
_
F
o
l
d
e
r
s
 
.
 
p
u
s
h
 
v
a
r
 
.
 
l
e
a
 
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
b
p
 
-
 
v
a
r
]
 
.
 
c
a
l
l
 
v
a
r
 
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
 
l
e
a
 
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
b
p
 
-
 
v
a
r
]
 
.
 
c
a
l
l
 
v
a
r
 
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