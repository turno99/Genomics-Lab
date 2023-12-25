seq1 = "ACAGA"
seq2 = "ACATA"

#seq1 = "ACACACTA"
#seq2 = "AGCACACA"
len1 = len(seq1)
len2 = len(seq2)

swapped = False
if len1<len2:
    len1, len2 = len2, len1
    seq1, seq2 = seq2, seq1
    swapped = True

gap_cost = -1
mismatch_cost = -3
match_cost = 10

rows = len1+1
cols = len2+1

table = [[0 for _ in range(cols)]for _ in range(rows)]

def build_table():
    for i in range(len1+1):
        table[i][0] = i * -5

    for j in range(len2+1):
        table[0][j] = j * -5
    
    for i in range(1,len1+1):
        for j in range(1,len2+1):
            table[i][j] = max(table[i-1][j-1]+evaluate(seq1[i-1],seq2[j-1]),table[i-1][j] + gap_cost, table[i][j-1] + gap_cost)



def evaluate(a, b):
    if a==b:
        return match_cost
    elif a=='-' or b=='-':
        return gap_cost
    else: return mismatch_cost

def traceback(seqA, seqB):
    ansAlignA = ""
    ansAlignB = ""
    i = len(seqA)
    j = len(seqB)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and table[i][j] == table[i - 1][j - 1] + evaluate(seqA[i - 1], seqB[j - 1]):
            ansAlignA += seqA[i - 1]
            ansAlignB += seqB[j - 1]
            i -= 1
            j -= 1
        elif i > 0 and table[i][j] == table[i - 1][j] + gap_cost:
            ansAlignA += seqA[i - 1]
            ansAlignB += "-"
            i -= 1
        else:
            ansAlignA += "-"
            ansAlignB += seqB[j - 1]
            j -= 1

        
    return ansAlignA, ansAlignB

build_table()
for row in table:
    print(table)
ans1, ans2 = traceback(seq1,seq2)
ans1 = ans1[::-1]
ans2 = ans2[::-1]
if swapped is True:
    ans1, ans2 = ans2, ans1
print(ans1)
print(ans2)

le = len(ans1)
cost = 0

for i in range(le):
    cost = cost + evaluate(ans1[i],ans2[i])

print(cost)