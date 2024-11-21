print("Bienvenido al sistema\n     ¡WorkSync!")
print("-------------------------------")
print("1. Iniciar sesión")
print("2. Registrarse")
print("-------------------------------")
choice = input("Ingrese su opción: ")
if choice == "1":
    print("Iniciando sesión...")
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    if username == "admin" and password == "admin":
        print("¡Bienvenido, administrador!")
    else:
        print("Nombre de usuario o contraseña incorrectos")
elif choice == "2":
        print("Registrando usuario...")
        username = input("Ingrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")
        print("¡Usuario creado con éxito!")
