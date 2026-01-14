#!/bin/bash
# Script para realizar backup de PostgreSQL

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/postgresql_backup_$TIMESTAMP.sql"

# Crear directorio de backups si no existe
mkdir -p $BACKUP_DIR

echo "🔄 Iniciando backup de PostgreSQL..."

# Realizar backup usando docker exec
docker exec medical_postgres pg_dump -U medical_user -d medical_appointments > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo " Backup completado exitosamente: $BACKUP_FILE"
    
    # Comprimir el backup
    gzip $BACKUP_FILE
    echo " Backup comprimido: $BACKUP_FILE.gz"
    
    # Mostrar tamaño del archivo
    ls -lh "$BACKUP_FILE.gz"
else
    echo " Error al realizar el backup"
    exit 1
fi