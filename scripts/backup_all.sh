#!/bin/bash
# Script para realizar backup completo del sistema

echo " Iniciando backup completo del sistema..."
echo "================================================"

# Backup PostgreSQL
echo ""
echo "1️  Realizando backup de PostgreSQL..."
./scripts/backup_postgresql.sh

if [ $? -ne 0 ]; then
    echo " Error en backup de PostgreSQL"
    exit 1
fi

# Backup MongoDB
echo ""
echo "2️ Realizando backup de MongoDB..."
./scripts/backup_mongodb.sh

if [ $? -ne 0 ]; then
    echo " Error en backup de MongoDB"
    exit 1
fi

echo ""
echo "================================================"
echo " Backup completo del sistema finalizado"
echo ""
echo " Archivos de backup generados en ./backups/"
ls -lh ./backups/ | tail -2