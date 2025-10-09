#!/bin/bash

DB_NAME="webcliente"

# Pedir credenciales root
read -p "Usuario root de MariaDB: " ROOT_USER
read -s -p "Password de root: " ROOT_PASS
echo ""

# Crear DB y tablas
mysql -u"$ROOT_USER" -p"$ROOT_PASS" <<EOF
DROP DATABASE IF EXISTS $DB_NAME;
CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE $DB_NAME;

-- Tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente',
    status BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Tabla de empresas
CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number CHAR(4) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de subcarpetas
CREATE TABLE subfolders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    path VARCHAR(500) NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Tabla de permisos
CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    company_id INT NOT NULL,
    subfolder_id INT NOT NULL,
    can_read BOOLEAN DEFAULT TRUE,
    can_write BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (subfolder_id) REFERENCES subfolders(id) ON DELETE CASCADE
);

-- Tabla de pedidos
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    company_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);
EOF

# -----------------------------
# Crear primer usuario admin
# -----------------------------
echo "=== Crear primer usuario admin ==="
read -p "Name: " ADMIN_NAME
read -p "Email: " ADMIN_EMAIL
read -s -p "Password: " ADMIN_PASS
echo ""

# Generar password Argon2 usando Python
ARGON2_PASS=$(python3 - <<END
from argon2 import PasswordHasher
ph = PasswordHasher()
print(ph.hash("$ADMIN_PASS"))
END
)

# Insertar en tabla users
mysql -u"$ROOT_USER" -p"$ROOT_PASS" $DB_NAME <<EOF
INSERT INTO users (name, email, password_hash, role, status)
VALUES ('$ADMIN_NAME', '$ADMIN_EMAIL', '$ARGON2_PASS', 'admin', TRUE);
EOF

# Crear usuario MariaDB para la web
read -p "Usuario DB a crear (para conectar la web): " DB_USER
read -s -p "Password de DB: " DB_USER_PASS
echo ""

mysql -u"$ROOT_USER" -p"$ROOT_PASS" <<EOF
CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_USER_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
EOF

echo "✅ Base de datos '$DB_NAME' recreada con tablas."
echo "✅ Usuario admin insertado en tabla users (Argon2)."
echo "✅ Usuario MariaDB '$DB_USER' creado con permisos."
