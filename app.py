from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Proyecto, Tarea

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gestion.db'
app.config['SECRET_KEY'] = 'cL4v3S3cr3t4'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    filtro_estado = request.args.get('estado')
    
    query = Proyecto.query
    
    if filtro_estado and filtro_estado != 'todos':
        query = query.filter_by(estado=filtro_estado)
        
    pagination = query.order_by(Proyecto.fecha_creacion.desc()).paginate(page=page, per_page=5)
    
    return render_template('index.html', pagination=pagination, filtro=filtro_estado)

@app.route('/projects/create', methods=['POST'])
def create_project():
    nombre = request.form.get('nombre')
    cliente = request.form.get('cliente')
    
    if nombre and cliente:
        nuevo = Proyecto(nombre=nombre, cliente=cliente)
        db.session.add(nuevo)
        db.session.commit()
        flash('Proyecto creado exitosamente', 'success')
    else:
        flash('Faltan datos obligatorios', 'danger')
        
    return redirect(url_for('index'))

@app.route('/projects/<int:id>')
def project_detail(id):
    proyecto = Proyecto.query.get_or_404(id)
    return render_template('detail.html', proyecto=proyecto)

@app.route('/projects/<int:id>/status', methods=['POST'])
def update_project_status(id):
    proyecto = Proyecto.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')
    
    if nuevo_estado == 'finalizado' and proyecto.tiene_tareas_pendientes():
        flash('Error: No se puede finalizar el proyecto porque tiene tareas pendientes o en progreso.', 'danger')
        return redirect(url_for('project_detail', id=id))
    
    proyecto.estado = nuevo_estado
    db.session.commit()
    flash(f'Estado actualizado a {nuevo_estado}', 'success')
    return redirect(url_for('project_detail', id=id))


@app.route('/projects/<int:project_id>/tasks', methods=['POST'])
def add_task(project_id):
    titulo = request.form.get('titulo')
    responsable = request.form.get('responsable')
    
    if titulo and responsable:
        nueva_tarea = Tarea(proyecto_id=project_id, titulo=titulo, responsable=responsable)
        db.session.add(nueva_tarea)
        db.session.commit()
        flash('Tarea agregada', 'success')
    
    return redirect(url_for('project_detail', id=project_id))

@app.route('/tasks/<int:id>/status', methods=['POST'])
def update_task_status(id):
    tarea = Tarea.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')
    
    tarea.estado = nuevo_estado
    db.session.commit()
    
    return redirect(url_for('project_detail', id=tarea.proyecto_id))

if __name__ == '__main__':
    app.run(debug=True)