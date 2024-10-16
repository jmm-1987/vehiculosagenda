from flask import render_template, request, redirect, url_for
import ftplib

def register_ftp_transfer_routes(app):
    @app.route('/ftp_transfer')
    def ftp_transfer():
        origen = ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "XPOsalidas"]
        lista_conexiones = [["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DSEL", "PODSalidasXPO/POD"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "GGSS", "PODSalidasXPO/PRIVADO"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "VARI", "PODSalidasXPO/PRIVADO"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DADR", "PODSalidasXPO/PRIVADO"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "ATRA", "PODSalidasXPO/POD"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DFIR", "PODSalidasXPO/POD"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DALB", "PODSalidasXPO/POD"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "POD", "PODSalidasXPO/POD"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "CONS", "PODSalidasXPO/POD"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "EREP", "PODSalidasXPO/POD"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "MANI", "PODSalidasXPO/POD"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "INCC", "PODSalidasXPO/INC"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "INCB", "PODSalidasXPO/INC"],
                            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DIMG", "PODSalidasXPO/INC"]]
        return render_template('ftp_transfer.html', origen=origen, conexiones=lista_conexiones)

    @app.route('/iniciar_transferencia', methods=['POST'])
    def iniciar_transferencia_route():
        # Recopilar los datos del formulario para la conexión de origen
        ftp_origen = request.form.get('ftp_origen')
        username_origen = request.form.get('username_origen')
        password_origen = request.form.get('password_origen')
        directory_origen = request.form.get('directory_origen')

        # Recoger las conexiones de destino (suponiendo que tienes un número variable de conexiones)
        lista_conexiones = []
        numero_conexiones = len(request.form) // 5  # Suponiendo 5 campos por conexión (FTP, usuario, password, prefijo, directorio)

        # Recopilar los datos de las conexiones de destino (suponiendo 5 campos por conexión)
        for i in range(1, numero_conexiones + 1):
            ftp_dest = request.form.get(f'ftp_dest_{i}')
            username_dest = request.form.get(f'username_dest_{i}')
            password_dest = request.form.get(f'password_dest_{i}')
            prefix_dest = request.form.get(f'prefix_dest_{i}')
            directory_dest = request.form.get(f'directory_dest_{i}')

            # Añadir cada conexión a la lista de conexiones
            lista_conexiones.append({
                'ftp': ftp_dest,
                'username': username_dest,
                'password': password_dest,
                'prefix': prefix_dest,
                'directory': directory_dest
            })

        # Lógica para iniciar la transferencia
        iniciar_transferencia({
            'origen': {
                'ftp': ftp_origen,
                'username': username_origen,
                'password': password_origen,
                'directory': directory_origen
            },
            'destinos': lista_conexiones
        })

        # Redirigir o mostrar un mensaje de éxito
        return redirect(url_for('ftp_transfer'))

    def iniciar_transferencia(datos):
        origen = datos['origen']
        destinos = datos['destinos']

        try:
            # Conectar al servidor de origen
            with ftplib.FTP(origen['ftp']) as ftp_origen:
                ftp_origen.login(origen['username'], origen['password'])
                ftp_origen.cwd(origen['directory'])

                # Listar los archivos en el directorio de origen
                archivos_origen = ftp_origen.nlst()  # Obtiene la lista de nombres de archivos

                # Transferir archivos a cada destino
                for destino in destinos:
                    with ftplib.FTP(destino['ftp']) as ftp_dest:
                        ftp_dest.login(destino['username'], destino['password'])
                        ftp_dest.cwd(destino['directory'])

                        # Iterar sobre los archivos de origen y verificar el prefijo
                        for archivo in archivos_origen:
                            if archivo.startswith(destino['prefix']):  # Verifica si el nombre del archivo empieza con el prefijo
                                print(f"Transferiendo {archivo} a {destino['directory']} en {destino['ftp']}")

                                # Descargar el archivo del servidor de origen temporalmente
                                with open(archivo, 'wb') as local_file:
                                    ftp_origen.retrbinary(f'RETR {archivo}', local_file.write)

                                # Subir el archivo al servidor de destino
                                with open(archivo, 'rb') as local_file:
                                    ftp_dest.storbinary(f'STOR {archivo}', local_file)

                                print(f"{archivo} transferido con éxito a {destino['directory']} en {destino['ftp']}")

                                # Borrar el archivo del servidor de origen
                                ftp_origen.delete(archivo)
                                print(f"{archivo} eliminado del servidor de origen.")

                            else:
                                print(f"El archivo {archivo} no coincide con el prefijo {destino['prefix']} de la conexión destino")

        except Exception as e:
            print(f"Error durante la transferencia: {e}")
