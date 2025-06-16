from datetime import datetime 
from flask import Flask, request, render_template 
from flask_sqlalchemy import SQLAlchemy 
#from werkzeug.security import generate_password_hash, check_password_hash



from models import db, Trabajador, RegistroHorario

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route('/')
def inicio():
	return render_template('inicio.html')



@app.route('/registrar_entrada', methods=['GET', 'POST'])


def registrarentrada():
    if request.method == 'POST': 
            
            trabajador = Trabajador.query.filter_by(legajo=request.form['legajo']).first()

            if trabajador is None:
                return render_template('error.html', error="Trabajador no encontrado, ingrese un legajo válido.")
            
            else:
                if (trabajador.dni)[-4:] != request.form['dni']:
                    return render_template('error.html', error="DNI incorrecto, ingrese un DNI válido.")
                
                else:
                    registro = RegistroHorario.query.filter_by(
                        fecha=datetime.now().date(),
                        idtrabajador=trabajador.id,
                    ).first()

                    if registro:
                        return render_template('error.html', error="Ya se registró una entrada para hoy, por favor intentélo de nuevo mañana, no se olvide de registrar su salida.")
                    else:
                        nuevo_registro = RegistroHorario(
                            fecha=datetime.now().date(),
                            horaentrada=datetime.now().time(),
                            horasalida=None,
                            dependencia= request.form['dependencia'],
                            idtrabajador=trabajador.id
                            )
    
                        db.session.add(nuevo_registro)
                        db.session.commit()
                        return render_template('aviso.html', mensaje="¡Entrada registrada exitosamente! Buen día :).")
    else:
        return render_template('registrar_entrada.html')


@app.route('/registrar_salida', methods=['GET', 'POST'])
def registrarsalida():
    if request.method == 'POST':
        
        if 'confirmar' in request.form:
            registro_id = request.form['registro_id']
            registro = RegistroHorario.query.get(registro_id)
            
            if not registro:
                return render_template('error.html', error="Registro no encontrado.")
            else:
                registro.horasalida = datetime.now().time()
                db.session.commit()
                return render_template('aviso.html', mensaje="¡Salida registrada exitosamente! Nos vemos pronto :)")
        else: 
            legajo = request.form.get('legajo')
            dni = request.form.get('dni')
            trabajador = Trabajador.query.filter_by(legajo=legajo).first()
            
            if trabajador is None:
                return render_template('error.html', error="Trabajador no encontrado, ingrese un legajo válido.")
            
            else:
                if (trabajador.dni)[-4:] != dni:
                    return render_template('error.html', error="DNI incorrecto, ingrese un DNI válido.")
                else:    
                    registro = RegistroHorario.query.filter_by(
                        idtrabajador=trabajador.id,
                        fecha=datetime.now().date(),
                        horasalida=None
                    ).first()
                    
                    if registro is None:
                        return render_template('error.html', error="No se encontró un registro de entrada para hoy, por favor registre su entrada primero.")
                    else:
                        return render_template('confirmar_salida.html', dependencia=registro.dependencia, registro_id=registro.id, legajo=trabajador.legajo, dni=trabajador.dni)

    else:        
        return render_template('registrar_salida.html')


@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    if request.method == 'POST':
        
        legajo = request.form['legajo']
        dni = request.form['dni']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

        trabajador = Trabajador.query.filter_by(legajo=legajo).first()
        if trabajador is None:
            return render_template('error.html', error="Trabajador no encontrado, ingrese un legajo válido.")
        else:
            
            if (trabajador.dni)[-4:] != dni:
                return render_template('error.html', error="DNI incorrecto, ingrese un DNI válido.")
            else:    
                registros = RegistroHorario.query.filter(
                    RegistroHorario.idtrabajador == trabajador.id,
                    RegistroHorario.fecha >= fecha_inicio,
                    RegistroHorario.fecha <= fecha_fin
                    ).order_by(RegistroHorario.fecha.desc()).all()

                if not registros:
                    return render_template('error.html', error="No se encontraron registros laborales en esas fechas.")
                else:
                    return render_template('consultar.html', registros=registros, trabajador=trabajador)

    else:
        return render_template('consultar.html')#

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 