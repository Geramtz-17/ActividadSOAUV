# soap_service.py
from spyne import Application, rpc, ServiceBase, Unicode, Integer, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from database import get_connection
import logging

logger = logging.getLogger("matriculas-soap")
logging.basicConfig(level=logging.INFO)

class Student(ComplexModel):
    studentId = Unicode
    givenName = Unicode
    familyName = Unicode
    email = Unicode

class Course(ComplexModel):
    courseId = Unicode
    title = Unicode
    term = Unicode

class MatriculaResponse(ComplexModel):
    message = Unicode
    enrollmentId = Unicode

class MatriculasService(ServiceBase):

    @rpc(Student, Course, _returns=MatriculaResponse)
    def EnrollStudent(ctx, student, course):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            name = f"{student.givenName} {student.familyName}"
            sql = "INSERT INTO matriculas (student_id, nombre, status) VALUES (%s, %s, %s)"
            cursor.execute(sql, (student.studentId, name, "ACTIVA"))
            conn.commit()
            enrollment_id = str(cursor.lastrowid)
            cursor.close()
            conn.close()
            return MatriculaResponse(message="OK", enrollmentId=enrollment_id)
        except Exception as e:
            logger.exception("Error EnrollStudent")
            return MatriculaResponse(message=f"Error: {str(e)}", enrollmentId="")

    @rpc(Integer, _returns=Unicode)
    def getMatricula(ctx, id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_id, nombre, status, created_at FROM matriculas WHERE id = %s", (id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                return f"ID: {row['id']}, StudentId: {row['student_id']}, Nombre: {row['nombre']}, Estado: {row['status']}, Creado: {row['created_at']}"
            return "Matrícula no encontrada"
        except Exception as e:
            logger.exception("Error getMatricula")
            return f"Error: {str(e)}"

    @rpc(Integer, _returns=Unicode)
    def cancelMatricula(ctx, id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE matriculas SET status = 'CANCELADA' WHERE id = %s", (id,))
            conn.commit()
            updated = cursor.rowcount
            cursor.close()
            conn.close()
            if updated > 0:
                return f"Matrícula {id} cancelada correctamente"
            else:
                return "No se encontró la matrícula"
        except Exception as e:
            logger.exception("Error cancelMatricula")
            return f"Error: {str(e)}"

soap_app = Application(
    [MatriculasService],
    tns='http://uv.mx/matriculas',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

soap_wsgi_app = WsgiApplication(soap_app)
