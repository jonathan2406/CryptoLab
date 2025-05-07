# Photon Heist Lab  
*(versión Beginner‑Friendly – Darkwall)*  

> **Objetivo docente:** Introducir a los estudiantes en técnicas de hacking web
> sencillas (recon, metadatos, cracking online, manipulación de cookies y XOR)
> usando sólo el navegador + sitios online.

---

## 0 · Historia

La startup energética **Photon Labs** perdió los planos de su celda fotónica.
Un empleado traidor dejó pistas dentro de un micro‑sitio Flask.  
El escuadrón **Darkwall** debe recolectar **6 flags** para restaurar el
“Photon Core”.

---

## 1 · Mapa rápido del flujo

| # | Técnica | Ruta / Archivo | Flag |
|---|---------|----------------|------|
| 0 | Recon – `robots.txt` | `/robots.txt` | `FLAG{recon_ready}` |
| 1 | EXIF → Base64 | `/backup/cell.jpg` | `FLAG{pixels_reveal}` |
| 2 | CrackStation (MD5) | Login con pass `secret` | `FLAG{hash_broken}` |
| 3 | Cookie tampering | Editar `role → admin`, `sig → nimda` | `FLAG{photon_escalated}` |
| 4 | SHA‑1 de flags (A‑Z) | `/unlock?key=<hash>` | `FLAG{photon_core_unlocked}` |
| 5 | XOR byte 0x42 | `core_blueprint.bin` | `FLAG{photon_heist_complete}` |

---

## 2 · Walk‑through detallado

1. **Recon**  
   Visitan `/robots.txt`. Comentario con primera flag + pista a `/backup/`.

2. **Metadatos**  
   Descargar `cell.jpg` → abrir en exif.tools → `UserComment` contiene  
   `MD5:5ebe2294ecd0e0f08eab7690d2a6ee69` (hash de “secret”) → flag 2.

3. **CrackStation**  
   Rompen el MD5 → password `secret` → formulario `/login` → cookie  
   ```json
   {role: user} -> {role: admin}
   ```
   FLAG{recon_ready}

markdown
Copiar
Editar

---

### **✅ Paso 2: Metadatos (EXIF)**

- Accede a la URL `/backup/` y descarga la imagen `cell.jpg`.
- Usa [exif.tools](https://exif.tools) para analizar los metadatos.
- Extrae el contenido del campo `UserComment`.  
Está codificado en **base64**.
- Al decodificar el mensaje base64 obtendrás:  
MD5:5ebe2294ecd0e0f08eab7690d2a6ee69

markdown
Copiar
Editar
- Encontraste la **FLAG 2** implícita aquí:  
FLAG{pixels_reveal}

yaml
Copiar
Editar

---

### **✅ Paso 3: Crackear Hash MD5**

- Usa [CrackStation](https://crackstation.net/) para romper el hash MD5:  
5ebe2294ecd0e0f08eab7690d2a6ee69

css
Copiar
Editar
- La contraseña resultante es:
secret

less
Copiar
Editar
- Usa esta contraseña (`secret`) para ingresar en la página `/login`.
- Dentro del código fuente HTML del login encontrarás oculta la **FLAG 3**:
FLAG{hash_broken}

yaml
Copiar
Editar

---

### **✅ Paso 4: Manipular Cookies (escalar privilegios)**

- Al hacer login exitoso, recibirás una cookie:
```json
{"uid":7,"role":"user","sig":"resu"}
```
Usa las DevTools del navegador (F12 > Application > Cookies) para cambiar:

Copiar
Editar
FLAG{photon_escalated}
También aparecerán instrucciones para el siguiente paso.

✅ Paso 5: SHA-1 Hashing
Copia las 4 flags anteriores:

Copiar
Editar
FLAG{recon_ready}
FLAG{pixels_reveal}
FLAG{hash_broken}
FLAG{photon_escalated}
Ordénalas alfabéticamente y pégalas sin espacios en una sola línea.

Calcula el SHA-1 resultante usando SHA1 Online.

Visita la URL:

bash
Copiar
Editar
/unlock?key=<tu_hash_sha1>
Si la clave SHA-1 es correcta, aparecerá la FLAG 5 en pantalla:

Copiar
Editar
FLAG{photon_core_unlocked}
✅ Paso 6 (final): Descifrar archivo binario XOR
Desde la misma página (/unlock), descarga el archivo:


core_blueprint.bin
Usa CyberChef:

Arrastra el archivo .bin.

Usa la operación XOR con clave: 0x42 (decimal 66).

Obtendrás como resultado el texto:

Photon Blueprint v1.0
FLAG{photon_heist_complete}
¡Has completado la misión!

📝 Entrega Final del Lab
Para finalizar exitosamente, deberás entregar la bandera final:

FLAG{photon_heist_complete}
Puedes realizar esta entrega mediante:

Un formulario proporcionado por tu profesor.

Captura de pantalla mostrando la bandera claramente.

# 🧑‍💻 Setup Rápido del Servidor (profesores):

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install flask pillow piexif
python app.py

