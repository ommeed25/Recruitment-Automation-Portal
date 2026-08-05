# import bcrypt

# password = "Admin@123"

# hashed = bcrypt.hashpw(
#     password.encode(),
#     bcrypt.gensalt()
# )

# print(hashed.decode())

import secrets

print(secrets.token_hex(32))