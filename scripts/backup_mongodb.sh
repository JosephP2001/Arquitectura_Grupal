#!/bin/bash
# Script para realizar backup de MongoDB

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="mongodb_backup_$TIMESTAMP"

# Crear directorio de backups si no existe
mkdir -p $BACKUP_DIR

echo " Iniciando backup de MongoDB..."

# Realizar backup usando mongodump
docker exec medical_mongodb mongodump \
    --username=mongo_user \
    --password=mongo_pass \
    --authenticationDatabase=admin \
    --db=medical_records \
    --out=/tmp/$BACKUP_NAME

# Copiar backup del contenedor al host
docker cp medical_mongodb:/tmp/$BACKUP_NAME $BACKUP_DIR/

if [ $? -eq 0 ]; then
    echo " Backup completado exitosamente: $BACKUP_DIR/$BACKUP_NAME"
    
    # Comprimir el backup
    cd $BACKUP_DIR
    tar -czf "$BACKUP_NAME.tar.gz" $BACKUP_NAME
    rm -rf $BACKUP_NAME
    cd ..
    
    echo " Backup comprimido: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
    
    # Mostrar tamaño del archivo
    ls -lh "$BACKUP_DIR/$BACKUP_NAME.tar.gz"
    
    # Limpiar backup temporal en el contenedor
    docker exec medical_mongodb rm -rf /tmp/$BACKUP_NAME
else
    echo " Error al realizar el backup"
    exit 1
fi