# # Autenticación de usuarios
# def autenticar_usuario():
#     from config.credenciales import usuarios
#     username = input("Usuario: ")
#     password = input("Contraseña: ")
#     if username in usuarios and usuarios[username]["password"] == password:
#         print(f"Bienvenido, {username} ({usuarios[username]['role']})")
#         return usuarios[username]["role"]
#     else:
#         print("Usuario o contraseña incorrectos.")
#         return None

from config.credenciales import usuarios

def autenticar_usuario():
    username = input("Usuario: ")
    password = input("Contraseña: ")
    if username in usuarios and usuarios[username]["password"] == password:
        print(f"Bienvenido, {username} ({usuarios[username]['role']})")
        return usuarios[username]["role"]
    else:
        print("Usuario o contraseña incorrectos.")
        return None