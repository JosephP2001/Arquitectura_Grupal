#!/bin/bash
# Script para restaurar backup de PostgreSQL

if [ -z "$1" ]; then
    echo " Uso: ./restore_postgresql.sh <archivo_backup.sql.gz>"
    echo "Ejemplo: ./restore_postgresql.sh backups/postgresql_backup_20260114_120000.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo " El archivo $BACKUP_FILE no existe"
    exit 1
fi

echo "🔄 Restaurando backup de PostgreSQL desde $BACKUP_FILE..."

# Descomprimir si es necesario
if [[ $BACKUP_FILE == *.gz ]]; then
    echo " Descomprimiendo archivo..."
    gunzip -k $BACKUP_FILE
    BACKUP_FILE="${BACKUP_FILE%.gz}"
fi

# Restaurar backup
docker exec -i medical_postgres psql -U medical_user -d medical_appointments < $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo " Restauración completada exitosamente"
else
    echo " Error al restaurar el backup"
    exit 1
fi