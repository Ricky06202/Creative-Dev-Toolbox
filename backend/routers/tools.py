from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import random
import colorsys
import re
from models import FormatRequest, RegexRequest, DataGenRequest

router = APIRouter(tags=["tools"])

@router.post("/format")
async def format_code(request: FormatRequest):
    if request.language == "json":
        import json
        try:
            parsed = json.loads(request.code)
            return {"formatted": json.dumps(parsed, indent=4)}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    
    elif request.language == "sql":
        import sqlparse
        try:
            return {"formatted": sqlparse.format(request.code, reindent=True, keyword_case='upper', indent_width=4)}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid SQL: {str(e)}")
            
    elif request.language == "html":
        from bs4 import BeautifulSoup
        try:
            soup = BeautifulSoup(request.code, "html.parser")
            return {"formatted": soup.prettify()}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid HTML: {str(e)}")

    elif request.language == "xml":
        from bs4 import BeautifulSoup
        try:
            soup = BeautifulSoup(request.code, "xml")
            return {"formatted": soup.prettify()}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid XML: {str(e)}")

    elif request.language in ["javascript", "js", "css"]:
        import jsbeautifier
        try:
            return {"formatted": jsbeautifier.beautify(request.code)}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid {request.language.upper()}: {str(e)}")

    elif request.language == "python":
        import autopep8
        try:
            return {"formatted": autopep8.fix_code(request.code)}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Python: {str(e)}")
    
    elif request.language in ["c", "cpp", "java", "csharp", "cs"]:
        import subprocess
        try:
            process = subprocess.Popen(
                ["clang-format", f"-assume-filename=file.{request.language}"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=request.code)
            if process.returncode == 0:
                return {"formatted": stdout}
            else:
                import jsbeautifier
                return {"formatted": jsbeautifier.beautify(request.code)}
        except Exception:
            try:
                import jsbeautifier
                return {"formatted": jsbeautifier.beautify(request.code)}
            except:
                return {"formatted": request.code}

    return {"formatted": request.code}

@router.post("/regex-explain")
async def explain_regex(request: RegexRequest):
    regex = request.regex
    explanations = []
    
    if regex.startswith("^"): explanations.append("🔍 **Inicio**: Debe empezar exactamente desde aquí.")
    if regex.endswith("$"): explanations.append("🏁 **Fin**: Debe terminar exactamente aquí.")
    if "\\d" in regex: explanations.append("🔢 **Dígitos**: Busca números (0-9).")
    if "\\w" in regex: explanations.append("🔤 **Alfanumérico**: Busca letras, números o guiones bajos.")
    if "\\s" in regex: explanations.append("⌴ **Espacios**: Busca espacios, tabulaciones o saltos de línea.")
    if "." in regex and "\\." not in regex: explanations.append("🃏 **Comodín**: El punto '.' coincide con cualquier carácter (excepto salto de línea).")
    if "*" in regex: explanations.append("♾️ **Cero o más**: El símbolo '*' indica que el elemento anterior puede repetirse indefinidamente o no estar.")
    if "+" in regex: explanations.append("➕ **Uno o más**: El símbolo '+' obliga a que el elemento anterior aparezca al menos una vez.")
    if "?" in regex: explanations.append("❓ **Opcional**: El símbolo '?' hace que el elemento anterior sea opcional.")
    if "{" in regex and "}" in regex: explanations.append("📏 **Rango**: Especificas exactamente cuántas veces quieres que se repita algo.")
    if "[" in regex and "]" in regex: explanations.append("📦 **Conjunto**: Los corchetes '[]' buscan cualquier carácter que esté dentro de ellos.")
    if "(" in regex and ")" in regex: explanations.append("👪 **Grupo**: Los paréntesis '()' agrupan partes del regex para tratarlas como una sola unidad.")
    
    if not explanations:
        explanations.append("Regex simple detectado. No se encontraron patrones complejos.")
        
    explanation_text = "\n".join(explanations)
    
    is_match = False
    match_details = ""
    if request.text:
        try:
            if re.fullmatch(regex, request.text):
                is_match = True
                match_details = f"🌟 **¡Coincidencia Total!**: El texto completo coincide perfectamente con el patrón.\n"
            else:
                matches = list(re.finditer(regex, request.text))
                if matches:
                    is_match = True
                    match_details = f"🔍 **Coincidencia Parcial**: El patrón se encontró {len(matches)} veces en el texto.\n"
                    match_details += "**Segmentos encontrados:**\n"
                    for i, m in enumerate(matches, 1):
                        match_details += f"- Coincidencia {i}: `{m.group(0)}` (posición {m.start()}-{m.end()})\n"
                else:
                    match_details = "❌ **Sin coincidencia**: El patrón no se encontró en ninguna parte del texto."
            
            first_match = re.search(regex, request.text)
            if first_match and first_match.groups():
                 match_details += f"\n📦 **Grupos capturados (primer match)**: {first_match.groups()}"
        except Exception as e:
            match_details = f"⚠️ **Error en el Regex**: {str(e)}"

    return {"explanation": explanation_text, "is_match": is_match, "match_details": match_details}

@router.post("/generate-data")
async def generate_data(request: DataGenRequest):
    from faker import Faker
    fake = Faker()
    data = []
    
    for _ in range(min(request.count, 100)):
        if request.type == "users":
            data.append({"name": fake.name(), "email": fake.email(), "job": fake.job(), "company": fake.company()})
        elif request.type == "emails":
            data.append(fake.email())
        elif request.type == "products":
            data.append({"name": fake.catch_phrase(), "price": fake.random_number(digits=3), "category": fake.word()})
        elif request.type == "profiles":
            data.append(fake.profile())
        elif request.type == "credit_cards":
            data.append({"card_number": fake.credit_card_number(), "provider": fake.credit_card_provider(), "expiry": fake.credit_card_expire()})
        elif request.type == "addresses":
            data.append({"address": fake.address(), "city": fake.city(), "country": fake.country(), "postal_code": fake.postcode()})
        elif request.type == "internet":
            data.append({"ip": fake.ipv4(), "user_agent": fake.user_agent(), "mac": fake.mac_address(), "url": fake.url()})
        elif request.type == "text":
            data.append({"paragraph": fake.paragraph(), "sentence": fake.sentence()})
        elif request.type == "dates":
            data.append({"date": fake.date(), "time": fake.time(), "date_time": fake.date_time().isoformat()})
            
    return {"data": data}

@router.get("/daily-palette")
async def get_daily_palette():
    return generate_random_palette("Cyber Sunset")

@router.post("/generate-palette")
async def generate_palette(base_colors: Optional[str] = None):
    return generate_random_palette(base_colors=base_colors)

def generate_random_palette(name: str = "Inspiración Aleatoria", base_colors: Optional[str] = None):
    def hex_to_hsl(hex_str):
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 3:
            hex_str = "".join([c*2 for c in hex_str])
        r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        return h*360, s*100, l*100

    def hsl_to_hex(h, s, l):
        r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
        return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))

    final_colors = []
    if base_colors:
        color_list = [c.strip() for c in base_colors.split(",") if c.strip()]
        for c in color_list:
            try:
                c = c if c.startswith("#") else f"#{c}"
                h, s, l = hex_to_hsl(c)
                final_colors.append(c)
            except: continue
        name = "Paleta Personalizada" if final_colors else name

    if not final_colors:
        h, s, l = random.randint(0, 360), 70, 60
        final_colors.append(hsl_to_hex(h, s, l))
    
    last_h, last_s, last_l = hex_to_hsl(final_colors[-1])
    while len(final_colors) < 5:
        next_h = (last_h + random.choice([30, -30, 180, 150, 210])) % 360
        next_s = max(10, min(90, last_s + random.randint(-20, 20)))
        next_l = max(10, min(90, last_l + random.randint(-20, 20)))
        final_colors.append(hsl_to_hex(next_h, next_s, next_l))
        last_h, last_s, last_l = next_h, next_s, next_l

    return {"colors": final_colors[:5], "name": name}

@router.get("/quotes")
async def get_quotes():
    quotes = [
        {"en": "First, solve the problem. Then, write the code.", "es": "Primero, resuelve el problema. Luego, escribe el código.", "author": "John Johnson"},
        {"en": "Clean code always looks like it was written by someone who cares.", "es": "El código limpio siempre parece escrito por alguien a quien le importa.", "author": "Robert C. Martin"},
        {"en": "Experience is the name everyone gives to their mistakes.", "es": "Experiencia es el nombre que todos dan a sus errores.", "author": "Oscar Wilde"},
        {"en": "Programming isn't about what you know; it's about what you can figure out.", "es": "Programar no es sobre lo que sabes; es sobre lo que puedes descifrar.", "author": "Chris Pine"},
        {"en": "The best way to predict the future is to invent it.", "es": "La mejor forma de predecir el futuro es inventarlo.", "author": "Alan Kay"},
        {"en": "Software is a great combination between artistry and engineering.", "es": "El software es una gran combinación entre arte e ingeniería.", "author": "Bill Gates"},
        {"en": "Talking is cheap. Show me the code.", "es": "Hablar es barato. Muéstrame el código.", "author": "Linus Torvalds"},
        {"en": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "es": "Cualquier tonto puede escribir código que un ordenador entienda. Los buenos programadores escriben código que los humanos entiendan.", "author": "Martin Fowler"}
    ]
    selected = random.choice(quotes)
    return {"quote_en": selected["en"], "quote_es": selected["es"], "author": selected["author"]}
