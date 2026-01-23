# Automatización de Reportes de Ventas

## *Sobre el proyecto*
Este sistema automático genera reportes de ventas en Excel y PDF usando datos reales, calcula indicadores clave (KPIs), crea gráficos y los envía por email. Ideal para las empresas y PYMEs que necesitan informes periódicos sin intervención manual.

## Beneficios para tu negocio
- Ahorra tiempo y esfuerzo cada mes.
- Genera reportes listos para dirección o reuniones.
- Los informes se envían automáticamente a tu correo. - Esta desactivado por defecto, pero lo hace al configurar al emisor y el receptor( Si lo haces usa variables de entorno para no exponer datos sensibles.) 
- Reduce errores de reportes manuales.

## ¿Cómo funciona?
1. Se descargan y limpian los datos.
2. Se calculan KPIs importantes (ventas totales, tendencia, etc.).
3. Se generan gráficos y un PDF ejecutivo.
4. Se exporta un Excel detallado.
5. Se envía el informe por email automáticamente.

##  Ejemplos de salida


##  Cómo probarlo
```bash
git clone https://github.com/juancaalcaraz/automatizacion-de-reportes-de-ventas.git
cd automatizacion-de-reportes-de-ventas
# instalar dependencias
pip install -r requirements.txt
# ejecutar
python main.py
```
# Sobre mí

Soy Técnico Superior en Ciencias de Datos e Inteligencia Artificial. Desarrollo soluciones de automatización para análisis y reporting, Creo dashboard para la toma de decisiones estratégicas y aplico soluciones de IA para los negocios que lo requieran.

## Fuente de datos

Los datos utilizados provienen del portal de Datos Abiertos del Gobierno de la República Argentina  
Dataset: [**Ventas en supermercados**](https://www.datos.gob.ar/sv/dataset/sspm-ventas-supermercados/archivo/sspm_455.1)

Fuente: https://datos.gob.ar  
Los datos se utilizan con fines demostrativos y educativos.


## Aviso legal:
> Los reportes y visualizaciones presentados son ejemplos generados a partir de datos abiertos y no representan información comercial confidencial.

