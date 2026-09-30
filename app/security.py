from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(password : str, hashed_password : str) -> bool:
    return password_hash.verify(password,hashed_password)




# password = "hello123"
# print("Password : ",password)
# hashed = hash_password(password)
# print("\nIt is hashed password : ",hashed,"\n")

# print(verify_password("hello123",hashed))

# print(verify_password("hello",hashed))
