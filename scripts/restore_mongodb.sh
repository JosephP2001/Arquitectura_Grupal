#!/bin/bash
# Script para restaurar backup de MongoDB

if [ -z "$1" ]; then
    echo " Uso: ./restore_mongodb.sh <archivo_backup.tar.gz>"
    echo "Ejemplo: ./restore_mongodb.sh backups/mongodb_backup_20260114_120000.tar.gz"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo " El archivo $BACKUP_FILE no existe"
    exit 1
fi

TEMP_DIR="./temp_restore"
mkdir -p $TEMP_DIR

echo " Restaurando backup de MongoDB desde $BACKUP_FILE..."

# Descomprimir backup
echo " Descomprimiendo archivo..."
tar -xzf $BACKUP_FILE -C $TEMP_DIR

# Obtener el nombre del directorio extraído
BACKUP_DIR=$(ls $TEMP_DIR | head -n 1)

# Copiar al contenedor
docker cp "$TEMP_DIR/$BACKUP_DIR" medical_mongodb:/tmp/

# Restaurar backup usando mongorestore
docker exec medical_mongodb mongorestore \
    --username=mongo_user \
    --password=mongo_pass \
    --authenticationDatabase=admin \
    --db=medical_records \
    --drop \
    /tmp/$BACKUP_DIR/medical_records

if [ $? -eq 0 ]; then
    echo " Restauración completada exitosamente"
    
    # Limpiar archivos temporales
    rm -rf $TEMP_DIR
    docker exec medical_mongodb rm -rf /tmp/$BACKUP_DIR
else
    echo " Error al restaurar el backup"
    rm -rf $TEMP_DIR
    exit 1
fi