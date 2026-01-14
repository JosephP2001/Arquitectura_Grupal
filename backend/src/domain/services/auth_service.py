"""
Servicio de dominio: AuthService
Contiene la lógica de negocio relacionada con autenticación y autorización
"""
import re
from typing import Tuple

class AuthService:
    """Servicio para gestionar la lógica de negocio de autenticación"""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Valida que una contraseña cumpla con los requisitos de seguridad
        Reglas:
        - Mínimo 8 caracteres
        - Al menos una letra mayúscula
        - Al menos una letra minúscula
        - Al menos un número
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if not re.search(r"[a-z]", password):
            return False, "La contraseña debe contener al menos una letra minúscula"
        
        if not re.search(r"[A-Z]", password):
            return False, "La contraseña debe contener al menos una letra mayúscula"
        
        if not re.search(r"\d", password):
            return False, "La contraseña debe contener al menos un número"
        
        return True, "Contraseña válida"
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Valida que un username sea válido
        Reglas:
        - Mínimo 3 caracteres
        - Máximo 20 caracteres
        - Solo letras, números y guiones bajos
        """
        if len(username) < 3:
            return False, "El username debe tener al menos 3 caracteres"
        
        if len(username) > 20:
            return False, "El username no puede tener más de 20 caracteres"
        
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False, "El username solo puede contener letras, números y guiones bajos"
        
        return True, "Username válido"
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Valida formato de email
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_regex, email):
            return False, "Formato de email inválido"
        
        return True, "Email válido"
    
    @staticmethod
    def can_user_perform_action(user_role: str, required_role: str) -> bool:
        """
        Verifica si un usuario puede realizar una acción según su rol
        Jerarquía: admin > doctor > patient
        """
        role_hierarchy = {
            "admin": 3,
            "doctor": 2,
            "patient": 1
        }
        
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level