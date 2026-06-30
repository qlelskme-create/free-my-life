# Guía de Contribución

¡Gracias por tu interés en contribuir a Free My Life!

## Antes de Comenzar

1. Fork el repositorio
2. Clona tu fork localmente
3. Crea una rama para tu feature: `git checkout -b feature/nombre-feature`

## Proceso de Contribución

### 1. Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pytest pytest-cov pylint

# Ejecutar tests
pytest tests/

# Verificar código
pylint **/*.py
```

### 2. Commits

Usa commits claros y descriptivos:

```bash
git commit -m "Agregar encriptación AES-256"
git commit -m "Corregir bug en autenticación 2FA"
git commit -m "Documentar API REST"
```

### 3. Push y Pull Request

```bash
git push origin feature/nombre-feature
```

Luego abre un Pull Request con:
- Descripción clara del cambio
- Razón del cambio
- Tests incluidos
- Documentación actualizada

## Estándares de Código

### Python

- Seguir PEP 8
- Usar type hints
- Documentar funciones con docstrings

```python
def encrypt(plaintext: str) -> str:
    """
    Encrypt plaintext using AES-256
    
    Args:
        plaintext: Text to encrypt
        
    Returns:
        Encrypted text
    """
    pass
```

### JavaScript

- Usar ES6+
- Nombrar funciones claramente
- Comentar código complejo

### HTML/CSS

- Usar semántica HTML5
- Seguir BEM para CSS
- Responsive design

## Testing

Todos los cambios deben incluir tests:

```bash
# Crear test
echo "def test_new_feature():" > tests/test_feature.py

# Ejecutar tests
pytest tests/test_feature.py -v

# Coverage
pytest --cov=. tests/
```

## Documentación

Actualizar documentación si es necesario:

- README.md
- docs/
- Docstrings en código

## Tipos de Contribución

### Reportar Bugs

Abre un Issue con:
- Descripción del bug
- Pasos para reproducir
- Resultado esperado vs actual
- Versión y SO

### Sugerir Features

Describe:
- El problema que resuelve
- Casos de uso
- Posible implementación

### Mejorar Documentación

Corrige typos, claridad, o agrega ejemplos.

### Código

Cualquier mejora de código es bienvenida:
- Optimizaciones
- Nuevas features
- Refactoring
- Tests

## Código de Conducta

- Sé respetuoso
- Escucha el feedback
- Reporta problemas apropiadamente
- Ayuda a otros

## Preguntas

- Abre un Issue con etiqueta "question"
- Participa en Discussions
- Contacta a los mantenedores

---

**¡Gracias por contribuir a Free My Life! 🚀**
