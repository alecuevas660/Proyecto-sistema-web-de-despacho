from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import smtplib
from email.mime.text import MIMEText


class EmailAPIView(APIView):
    def post(self, request):
        # Llama a la función para enviar el correo
        result = enviar_correo()
        if result:
            return Response({'message': 'Correo Enviado Con Exito'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Error al enviar el correo.'}, status=status.HTTP_400_BAD_REQUEST)
        
        

class enviar_correo():
        
        recibidor = str

        sender = 'test.dummy4520@gmail.com'
        receiver =  recibidor
        password = 'uyvr oron kbwu mtqz'

        msg = MIMEText('Este es un mensaje de prueba desde un script simple.')
        msg['Subject'] = 'Prueba de correo'
        msg['From'] = sender
        msg['To'] = receiver

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
                print("Correo enviado exitosamente.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")