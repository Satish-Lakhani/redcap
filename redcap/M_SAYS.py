#! /usr/bin/python
# -*- coding: utf-8 -*-

#tupla di regex per individuare le parole da censurare
censura=["n[o0]+b",
"n(iu|u|[a@])bb[o0]",
"\bc[a@][mn]p",
"l[a@]m(ah|er)",
"c[o0]gl[i1][o0]n",
"b[o0](cc|kk)hin",
"m[o0]r[0o]n",
"p[o0]mp[i1]n",
"[a@][s$]{2}h[o0]le",
"f[uo0\*]ck",
"m[a@]rr?ic[o0]n",
"c[o0]nn[a@]rd",
"m[3e]rd",
"tr[o0][yi][a@]",
"putt[a@]n[a@]",
"che[a@]t",
"\bci(t+)",
"h[a@]ck",
"a[1i]mb",
"str[o0]nz",
"tu[@a] m[a@]dr[3e]",
"(k(u|o)|qu?)rw(a|o|y)?",
"s?pierd(ala(j|j?my)|ol(a|ic|ec)?)",
"f[i1]gl[i1][o0] d[1i]",
"[a@]ff[a@]n[ck]u",
"c[a@]mp[3e]r$"
]



#TODO aggiungere riconoscimento di frasi standard