# Photon Heist Lab - Soluciones

## Flags y Ubicaciones

1. **FLAG{recon_ready}**

   - Ubicación: `/robots.txt`
   - Método: Acceder directamente a la ruta

2. **FLAG{pixels_reveal}**

   - Ubicación: EXIF de `cell.jpg`
   - Método: Examinar los metadatos EXIF de la imagen

3. **FLAG{hash_broken}**

   - Ubicación: Comentario HTML en `login.html`
   - Método: Inspeccionar el código fuente

4. **FLAG{photon_escalated}**

   - Ubicación: API `/api/check` con cookie modificada
   - Método:
     1. Modificar la cookie para cambiar `role` a "admin"
     2. Calcular `sig` como "nimda" (role al revés)
     3. Enviar solicitud a `/api/check?sig=nimda`

5. **FLAG{photon_core_unlocked}**

   - Ubicación: `/unlock` con hash SHA-1 correcto
   - Método:
     1. Recolectar las 4 banderas anteriores
     2. Ordenarlas alfabéticamente
     3. Concatenar sin espacios
     4. Calcular SHA-1
     5. Acceder a `/unlock?key=<hash>`

6. **FLAG{photon_heist_complete}**
   - Ubicación: Contenido de `core_blueprint.bin`
   - Método:
     1. Descargar el archivo
     2. XOR cada byte con 0x42
     3. Leer el contenido descifrado

## Notas para Profesores

- El lab está diseñado para enseñar conceptos de:

  - Reconocimiento web
  - Metadatos y EXIF
  - Manipulación de cookies
  - Criptografía básica (XOR)
  - Hashing y verificación
  - Seguridad de APIs

- Los estudiantes deben seguir un proceso paso a paso para descubrir cada flag
- No hay soluciones directas en el código fuente
- El lab es auto-contenido y no requiere configuración adicional
