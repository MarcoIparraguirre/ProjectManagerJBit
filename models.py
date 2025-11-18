from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    # Estados: 'activo', 'pausado', 'finalizado'
    estado = db.Column(db.String(20), default='activo')
    
    # Relación con Tareas
    tareas = db.relationship('Tarea', backref='proyecto', lazy=True, cascade="all, delete-orphan")

    def tiene_tareas_pendientes(self):
        """Regla de negocio: Verifica si hay tareas que no estén 'hecha'"""
        for tarea in self.tareas:
            if tarea.estado != 'hecha':
                return True
        return False

class Tarea(db.Model):
    __tablename__ = 'tareas'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    # Estados: 'pendiente', 'en_progreso', 'hecha'
    estado = db.Column(db.String(20), default='pendiente')