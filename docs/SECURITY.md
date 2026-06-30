# Guía de Seguridad - Free My Life

## Características de Seguridad

### 1. Encriptación AES-256

Free My Life utiliza encriptación AES-256 de nivel militar para proteger tus datos:

- **Algoritmo**: Fernet (basado en AES)
- **Modo**: CBC con HMAC
- **Derivación de clave**: PBKDF2 con SHA-256

### 2. Hashing de Contraseñas

Las contraseñas se almacenan de forma segura:

- **Algoritmo**: bcrypt
- **Rondas**: 12
- **Salt**: Generado aleatoriamente

### 3. Autenticación de Dos Factores (2FA)

Protección adicional con:

- **Método**: TOTP (Time-based One-Time Password)
- **Estándar**: RFC 6238
- **Códigos QR**: Para fácil sincronización

### 4. HTTPS/SSL

- Todas las conexiones se encriptan
- Certificados SSL válidos
- HSTS habilitado en producción

### 5. Control de Sesión

- **Duración**: 1 hora de inactividad
- **Cookies seguras**: HttpOnly, Secure, SameSite
- **Token CSRF**: Protección contra ataques cross-site

### 6. Firewall

- **Monitoreo de red**: Conexiones activas
- **Detección de IP sospechosas**: Lista de bloqueo
- **Protección de puertos**: Puertos maliciosos bloqueados
- **Registro de actividad**: Auditoría completa

## Mejores Prácticas

### Configuración Segura

1. **Cambiar la clave secreta**:
   ```bash
   # Generar nueva clave
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Actualizar en `.env`

2. **Usar HTTPS en producción**:
   - Obtener certificado SSL (Let's Encrypt)
   - Configurar Nginx/Apache con SSL

3. **Mantener dependencias actualizadas**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Gestión de Credenciales

1. **Contraseñas fuertes**:
   - Mínimo 8 caracteres
   - Combinar mayúsculas, minúsculas, números, símbolos
   - No reutilizar contraseñas

2. **Habilitar 2FA**:
   - Obligatorio para cuentas administrativas
   - Usar aplicación autenticadora (Google Authenticator, Authy)

3. **Gestionar API Keys**:
   - Rotarlas regularmente
   - Usar diferentes claves para diferentes servicios

### Monitoreo

1. **Revisar logs regularmente**:
   ```bash
   tail -f logs/app.log
   ```

2. **Monitorear actividad sospechosa**:
   - Dashboard de Firewall
   - Alertas de intentos fallidos de login

3. **Auditoría de cambios**:
   - Todas las operaciones se registran
   - Verificar accesos no autorizados

## Vulnerabilidades Conocidas

### Mitigadas

- ✓ SQL Injection: Uso de ORM (SQLAlchemy)
- ✓ XSS: Templates con escape automático
- ✓ CSRF: Tokens CSRF en formularios
- ✓ Brute Force: Rate limiting y bloqueo de cuenta

### En Desarrollo

- [ ] Rate limiting más granular
- [ ] WAF (Web Application Firewall)
- [ ] Encriptación de base de datos

## Reportar Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad, **NO** la publiques en GitHub.

**En su lugar**, envía un correo a: `security@free-my-life.local`

Incluye:
- Descripción de la vulnerabilidad
- Pasos para reproducir
- Impacto potencial
- Versión afectada

## Cumplimiento

Free My Life cumple con:

- OWASP Top 10
- GDPR (Protección de datos)
- Estándares de criptografía modernos

## Recursos de Seguridad

- [OWASP](https://owasp.org/)
- [CWE](https://cwe.mitre.org/)
- [Criptografía](https://cryptography.io/)
- [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)
