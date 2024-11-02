from py_ecc.bn128 import is_on_curve, FQ
from py_ecc.fields import field_properties
field_mod = field_properties["bn128"]["field_modulus"]
from hashlib import sha256
from libnum import has_sqrtmod_prime_power, sqrtmod_prime_power

b = 3 # for bn128, y^2 = x^3 + 3
seed = "RareSkills"

x = int(sha256(seed.encode('ascii')).hexdigest(), 16) % field_mod 

entropy = 0

vector_basis = []
# modify the code below to generate n points
n = 4

for _ in range(n):
    while not has_sqrtmod_prime_power((x**3 + b) % field_mod, field_mod, 1):
        # increment x, so hopefully we are on the curve
        x = (x + 1) % field_mod
        entropy = entropy + 1

    # pick the upper or lower point depending on if entropy is even or odd
    y = list(sqrtmod_prime_power((x**3 + b) % field_mod, field_mod, 1))[entropy & 1 == 0]
    point = (FQ(x), FQ(y))
    assert is_on_curve(point, b), "sanity check"
    vector_basis.append(point)

    # new x value
    x = int(sha256(str(x).encode('ascii')).hexdigest(), 16) % field_mod 
print(vector_basis)

####### Answers of the questions from the book #######

# 1.If we used the same G1..Gn for both vectors before adding them, how could a committer open two different vectors for C3? 
#   Give an example. How does using a different set of points H1..Hn
#   prevent this?

# If same points are used then [v1,v2..,vn] and [w1,w2..,wn] can be exchanged index-wise and thus the commitment can be forged by the committer
# Example: send [w1,v2,..wn] and [v1,w2..vn] instead of [v1,v2..,vn] and [w1,w2..,wn]
# As discrete logarithm relation between G and H is unknown, committer won't be able to forge the opening in any case

# 2.What happens if the committer tries to switch the same elements inside the vector?
