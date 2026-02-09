"""
Servicio de Notificaciones para alertas del Service Registry
Soporta Email (SendGrid) y SMS (Twilio)
"""
import os
from datetime import datetime
from typing import Optional, List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
# from twilio.rest import Client  # Descomentar si se usa Twilio


class NotificationService:
    """Servicio para enviar notificaciones de cambios en servicios"""
    
    def __init__(self):
        # Configuración de SendGrid
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("SENDGRID_FROM_EMAIL", "notifications@medical-system.com")
        self.notification_email = os.getenv("NOTIFICATION_EMAIL", "admin@medical-system.com")
        
        # Configuración de Twilio (opcional)
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
        
        # Cliente de SendGrid
        self.sendgrid_client = None
        if self.sendgrid_api_key and self.sendgrid_api_key != "your_sendgrid_api_key_here":
            try:
                self.sendgrid_client = SendGridAPIClient(self.sendgrid_api_key)
                print("✅ SendGrid configurado correctamente")
            except Exception as e:
                print(f"⚠️ Error al configurar SendGrid: {e}")
        else:
            print("⚠️ SendGrid no configurado - Las notificaciones por email estarán deshabilitadas")
        
        # Cliente de Twilio (opcional)
        self.twilio_client = None
        # Descomentar si se usa Twilio:
        # if self.twilio_account_sid and self.twilio_auth_token:
        #     try:
        #         self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        #         print("✅ Twilio configurado correctamente")
        #     except Exception as e:
        #         print(f"⚠️ Error al configurar Twilio: {e}")
    
    def send_service_down_alert(
        self, 
        service_name: str, 
        error_message: Optional[str] = None,
        recipients: Optional[List[str]] = None
    ) -> bool:
        """
        Enviar alerta cuando un servicio cae
        
        Args:
            service_name: Nombre del servicio
            error_message: Mensaje de error opcional
            recipients: Lista de emails (usa default si es None)
        
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        subject = f"🔴 ALERTA: Servicio {service_name} CAÍDO"
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #e74c3c; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f8f9fa; }}
                .footer {{ padding: 10px; text-align: center; color: #666; font-size: 12px; }}
                .alert-box {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔴 Servicio Caído</h1>
                </div>
                <div class="content">
                    <p><strong>Sistema de Monitoreo - Medical Appointment Platform</strong></p>
                    <p>Se ha detectado que el siguiente servicio está CAÍDO:</p>
                    
                    <div class="alert-box">
                        <p><strong>Servicio:</strong> {service_name}</p>
                        <p><strong>Estado:</strong> DOWN</p>
                        <p><strong>Timestamp:</strong> {timestamp}</p>
                        {f'<p><strong>Error:</strong> {error_message}</p>' if error_message else ''}
                    </div>
                    
                    <p><strong>Acciones recomendadas:</strong></p>
                    <ul>
                        <li>Verificar el estado del contenedor Docker</li>
                        <li>Revisar los logs del servicio</li>
                        <li>Comprobar la conectividad de red</li>
                        <li>Reiniciar el servicio si es necesario</li>
                    </ul>
                    
                    <p><em>Este es un mensaje automático del sistema de monitoreo.</em></p>
                </div>
                <div class="footer">
                    <p>Medical Appointment Platform - Service Registry</p>
                    <p>Para más información, accede al dashboard de monitoreo</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(subject, html_content, recipients)
    
    def send_service_recovered_alert(
        self, 
        service_name: str,
        downtime_minutes: Optional[float] = None,
        recipients: Optional[List[str]] = None
    ) -> bool:
        """
        Enviar alerta cuando un servicio se recupera
        
        Args:
            service_name: Nombre del servicio
            downtime_minutes: Tiempo de inactividad en minutos
            recipients: Lista de emails (usa default si es None)
        
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        subject = f"🟢 Servicio {service_name} RECUPERADO"
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        downtime_str = f"{downtime_minutes:.2f} minutos" if downtime_minutes else "desconocido"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2ecc71; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f8f9fa; }}
                .footer {{ padding: 10px; text-align: center; color: #666; font-size: 12px; }}
                .success-box {{ background-color: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🟢 Servicio Recuperado</h1>
                </div>
                <div class="content">
                    <p><strong>Sistema de Monitoreo - Medical Appointment Platform</strong></p>
                    <p>El siguiente servicio se ha RECUPERADO y está funcionando normalmente:</p>
                    
                    <div class="success-box">
                        <p><strong>Servicio:</strong> {service_name}</p>
                        <p><strong>Estado:</strong> UP</p>
                        <p><strong>Timestamp:</strong> {timestamp}</p>
                        <p><strong>Tiempo de inactividad:</strong> {downtime_str}</p>
                    </div>
                    
                    <p>El servicio está operando normalmente y aceptando conexiones.</p>
                    
                    <p><em>Este es un mensaje automático del sistema de monitoreo.</em></p>
                </div>
                <div class="footer">
                    <p>Medical Appointment Platform - Service Registry</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(subject, html_content, recipients)
    
    def send_service_degraded_alert(
        self, 
        service_name: str,
        reason: Optional[str] = None,
        recipients: Optional[List[str]] = None
    ) -> bool:
        """
        Enviar alerta cuando un servicio está degradado
        
        Args:
            service_name: Nombre del servicio
            reason: Razón de la degradación
            recipients: Lista de emails (usa default si es None)
        
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        subject = f"🟡 ADVERTENCIA: Servicio {service_name} DEGRADADO"
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f39c12; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f8f9fa; }}
                .footer {{ padding: 10px; text-align: center; color: #666; font-size: 12px; }}
                .warning-box {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🟡 Servicio Degradado</h1>
                </div>
                <div class="content">
                    <p><strong>Sistema de Monitoreo - Medical Appointment Platform</strong></p>
                    <p>El siguiente servicio está experimentando problemas de rendimiento:</p>
                    
                    <div class="warning-box">
                        <p><strong>Servicio:</strong> {service_name}</p>
                        <p><strong>Estado:</strong> DEGRADED</p>
                        <p><strong>Timestamp:</strong> {timestamp}</p>
                        {f'<p><strong>Razón:</strong> {reason}</p>' if reason else ''}
                    </div>
                    
                    <p>El servicio sigue funcionando pero con rendimiento reducido. Se recomienda monitorear de cerca.</p>
                    
                    <p><em>Este es un mensaje automático del sistema de monitoreo.</em></p>
                </div>
                <div class="footer">
                    <p>Medical Appointment Platform - Service Registry</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(subject, html_content, recipients)
    
    def _send_email(
        self, 
        subject: str, 
        html_content: str, 
        recipients: Optional[List[str]] = None
    ) -> bool:
        """
        Método privado para enviar email vía SendGrid
        
        Args:
            subject: Asunto del email
            html_content: Contenido HTML
            recipients: Lista de destinatarios
        
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        if not self.sendgrid_client:
            print(f"⚠️ Email no enviado (SendGrid no configurado): {subject}")
            # En modo desarrollo, solo logear
            print(f"📧 [SIMULADO] Email: {subject}")
            return False
        
        try:
            # Usar email por defecto si no se especifican destinatarios
            to_emails = recipients or [self.notification_email]
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_emails,
                subject=subject,
                html_content=html_content
            )
            
            response = self.sendgrid_client.send(message)
            
            if response.status_code >= 200 and response.status_code < 300:
                print(f"✅ Email enviado: {subject}")
                return True
            else:
                print(f"⚠️ Error al enviar email: Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error al enviar email: {e}")
            return False
    
    def send_sms(self, message: str, phone_number: Optional[str] = None) -> bool:
        """
        Enviar SMS vía Twilio (opcional)
        
        Args:
            message: Mensaje a enviar
            phone_number: Número de destino (usa default si es None)
        
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        if not self.twilio_client:
            print(f"⚠️ SMS no enviado (Twilio no configurado): {message}")
            # En modo desarrollo, solo simular
            print(f"📱 [SIMULADO] SMS: {message}")
            return False
        
        # Implementación real de Twilio:
        # try:
        #     message = self.twilio_client.messages.create(
        #         body=message,
        #         from_=self.twilio_phone,
        #         to=phone_number or self.default_phone
        #     )
        #     print(f"✅ SMS enviado: {message.sid}")
        #     return True
        # except Exception as e:
        #     print(f"❌ Error al enviar SMS: {e}")
        #     return False
        
        return False


# Singleton
notification_service = NotificationService()