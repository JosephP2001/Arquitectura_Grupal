#!/bin/bash
# Script para dar permisos de ejecución a todos los scripts

echo "🔧 Configurando permisos de ejecución para scripts..."

chmod +x scripts/backup_postgresql.sh
chmod +x scripts/restore_postgresql.sh
chmod +x scripts/backup_mongodb.sh
chmod +x scripts/restore_mongodb.sh
chmod +x scripts/backup_all.sh

echo "✅ Permisos configurados correctamente"
echo ""
echo "Scripts disponibles:"
echo "  - ./scripts/backup_postgresql.sh"
echo "  - ./scripts/restore_postgresql.sh"
echo "  - ./scripts/backup_mongodb.sh"
echo "  - ./scripts/restore_mongodb.sh"
echo "  - ./scripts/backup_all.sh"