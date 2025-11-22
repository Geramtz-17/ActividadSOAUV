-- Schema: uav (ejecutar en MySQL)
CREATE DATABASE IF NOT EXISTS uav;
USE uav;

-- Programs
CREATE TABLE IF NOT EXISTS programs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(20) UNIQUE,
  name VARCHAR(200) NOT NULL
);

-- Students
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(50) UNIQUE,
  given_name VARCHAR(100),
  family_name VARCHAR(100),
  email VARCHAR(150),
  program_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE SET NULL
);

-- Courses
CREATE TABLE IF NOT EXISTS courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_id VARCHAR(50) UNIQUE,
  title VARCHAR(255) NOT NULL,
  credits INT DEFAULT 0,
  term VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Matriculas (enrollments)
CREATE TABLE IF NOT EXISTS matriculas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  course_id INT NOT NULL,
  status VARCHAR(20) DEFAULT 'ACTIVA',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Grades
CREATE TABLE IF NOT EXISTS grades (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  course_id INT NOT NULL,
  grade DECIMAL(5,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Datos de ejemplo
INSERT INTO programs (code, name) VALUES ('IS','Ingeniería en Sistemas'), ('ARQ','Arquitectura');

INSERT INTO students (student_id, given_name, family_name, email, program_id)
VALUES ('UV2025001','Juan','Perez','juan@uv.mx',1),
       ('UV2025002','Maria','Lopez','maria@uv.mx',1);

INSERT INTO courses (course_id, title, credits, term)
VALUES ('CS101','Introducción a la Programación',5,'2025-1'),
       ('MA101','Cálculo I',5,'2025-1');

INSERT INTO matriculas (student_id, course_id, status)
VALUES (1,1,'ACTIVA'), (2,1,'ACTIVA');

INSERT INTO grades (student_id, course_id, grade) VALUES
(1,1,8.5),(1,2,7.0),(2,1,9.0);
