import sys 
file=open(sys.argv[1])
def compute_opt(sequence, i, j, memo, pair):
    if j - i <= 4:
        return 0
    if memo[i][j] is not None:
        return memo[i][j]

    memo[i][j] = compute_opt(sequence, i, j - 1, memo, pair)
    for t in range(i, j - 4):
        if sequence[t] == pair.get(sequence[j], ''):
            score = 1 + compute_opt(sequence, i, t - 1, memo, pair) + compute_opt(sequence, t + 1, j - 1, memo, pair)
            if score > memo[i][j]:
                memo[i][j] = score
                memo[j][i] = t  
    return memo[i][j]

def rna_folding(sequence):
    n = len(sequence)
    memo = [[None] * n for _ in range(n)]
    pair = {'A': 'U', 'U': 'A', 'C': 'G', 'G': 'C'}
    compute_opt(sequence, 0, n - 1, memo, pair)

    def get_pairs(i, j):
        if j - i <= 4 or memo[i][j] is None:
            return []
        if memo[j][i] is not None:
            t = memo[j][i]
            return [(t, j)] + get_pairs(i, t - 1) + get_pairs(t + 1, j - 1)
        return get_pairs(i, j - 1)

    pairs = get_pairs(0, n - 1)
    return pairs, memo[0][n - 1]
s_name=''
print(f"Folding RNA in file {sys.argv[1]}\n")
s=''
for i in file: 
    if '**' in i:
       s=i.strip()
    elif 'A' in i or 'U' in i or 'C' in i:
        
        print(f'{s[0:2]} {s[2:-1]}, length={len(i.strip())}, Optimal secondary structure:')
        sequence = i
        pairs, max_pairs = rna_folding(sequence)
        pairs.sort()
        for i, j in pairs:
            print(f"{sequence[i]}-{sequence[j]} ({i + 1},{j + 1})")
        print(f"Total number of base pairs: {max_pairs}\n")
print("By Satish Dodda")

