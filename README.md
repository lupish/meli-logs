# meli-logs

Obtiene los logs de la traza de los usuarios. Realiza una limpieza quitando registros duplicados, nulos, usuarios con ID inválido y fechas inválidas.  
Detecta anomalías basadas en el login: login repetido o acciones que requieren login previo (logout, purchase, update_profile).  
Finalmente, obtiene el top 5 de usuarios con más acciones únicas en el último mes.

## Requisitos

Las librerías necesarias están listadas en `requirements.txt`. Para instalarlas, ejecutar:

```bash
pip install -r requirements.txt