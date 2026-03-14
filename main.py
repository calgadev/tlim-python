import json
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models.database import engine, Base, SessionLocal
from models import item, creature, inventory, bestiary
from routers import hunt, bestiary as bestiary_router, inventory as inventory_router, items
from services.sale_decision_service import gerar_relatorio_venda
from services.bestiary_service import get_progresso_bestiary, get_total_charm_points
from services.charm_calculator_service import calcular_sugestoes_charm, listar_charms
from parsers.json_hunt_parser import parse_json_hunt
from parsers.text_hunt_parser import parse_text_hunt
from models.item import Item
from models.creature import Creature
from models.inventory import UserInventory
from models.bestiary import BestiaryEntry

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TLIM - Tibia Loot & Inventory Manager",
    description="Gerencie seu loot e bestiário do Tibia",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(hunt.router)
app.include_router(bestiary_router.router)
app.include_router(inventory_router.router)
app.include_router(items.router)

USER_ID = 1

# ── Páginas HTML ─────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()
    try:
        inv = db.query(UserInventory).filter(UserInventory.user_id == USER_ID).all()
        total_value = sum(
            (db.query(Item).filter(Item.id == e.item_id).first().npc_price or 0) * e.quantity
            for e in inv
        )
        progresso = get_progresso_bestiary(db, USER_ID)
        total_pontos = get_total_charm_points(db, USER_ID)
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "active": "dashboard",
            "total_items": len(inv),
            "total_value": total_value,
            "total_creatures": len(progresso),
            "completed_creatures": sum(1 for c in progresso if c["completed"]),
            "total_charm_points": total_pontos,
        })
    finally:
        db.close()

@app.get("/import", response_class=HTMLResponse)
def import_page(request: Request):
    return templates.TemplateResponse("import.html", {
        "request": request,
        "active": "import"
    })

@app.post("/import/json")
async def import_json_html(request: Request, file: UploadFile = File(...)):
    db = SessionLocal()
    try:
        conteudo = await file.read()
        data = json.loads(conteudo)
        hunt_data = parse_json_hunt(data)
        relatorio = _processar_hunt_html(hunt_data, db)
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "active": "dashboard",
            **relatorio
        })
    except Exception as e:
        return templates.TemplateResponse("import.html", {
            "request": request,
            "active": "import",
            "error": f"Erro ao processar JSON: {str(e)}"
        })
    finally:
        db.close()

@app.post("/import/text")
async def import_text_html(request: Request, text: str = Form(...)):
    db = SessionLocal()
    try:
        hunt_data = parse_text_hunt(text)
        relatorio = _processar_hunt_html(hunt_data, db)
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "active": "dashboard",
            **relatorio
        })
    except Exception as e:
        return templates.TemplateResponse("import.html", {
            "request": request,
            "active": "import",
            "error": f"Erro ao processar texto: {str(e)}"
        })
    finally:
        db.close()

@app.get("/bestiary", response_class=HTMLResponse)
def bestiary_page(request: Request):
    db = SessionLocal()
    try:
        progresso = get_progresso_bestiary(db, USER_ID)
        total_pontos = get_total_charm_points(db, USER_ID)
        charms = listar_charms()
        return templates.TemplateResponse("bestiary.html", {
            "request": request,
            "active": "bestiary",
            "creatures": progresso,
            "total_charm_points": total_pontos,
            "charms": charms,
        })
    finally:
        db.close()

@app.get("/bestiary/charm", response_class=HTMLResponse)
def bestiary_charm(request: Request, charm: str = ""):
    db = SessionLocal()
    try:
        progresso = get_progresso_bestiary(db, USER_ID)
        total_pontos = get_total_charm_points(db, USER_ID)
        charms = listar_charms()
        charm_result = calcular_sugestoes_charm(charm, db, USER_ID) if charm else None
        if charm_result and "erro" in charm_result:
            charm_result = None
        return templates.TemplateResponse("bestiary.html", {
            "request": request,
            "active": "bestiary",
            "creatures": progresso,
            "total_charm_points": total_pontos,
            "charms": charms,
            "selected_charm": charm,
            "charm_result": charm_result,
        })
    finally:
        db.close()

@app.get("/inventory", response_class=HTMLResponse)
def inventory_page(request: Request):
    db = SessionLocal()
    try:
        entradas = db.query(UserInventory).filter(
            UserInventory.user_id == USER_ID
        ).all()
        resultado = []
        total_value = 0
        for entrada in entradas:
            it = db.query(Item).filter(Item.id == entrada.item_id).first()
            if not it:
                continue
            val = it.npc_price * entrada.quantity
            total_value += val
            resultado.append({
                "item": it.name,
                "quantity": entrada.quantity,
                "goal_quantity": entrada.goal_quantity,
                "goal_reached": entrada.quantity >= entrada.goal_quantity if entrada.goal_quantity > 0 else None,
                "npc_price": it.npc_price,
                "npc_seller": it.npc_seller,
                "is_imbuement_material": it.is_imbuement_material,
                "imbuement_name": it.imbuement_name,
                "estimated_value": val
            })
        resultado.sort(key=lambda x: x["estimated_value"], reverse=True)
        return templates.TemplateResponse("inventory.html", {
            "request": request,
            "active": "inventory",
            "items": resultado,
            "total_value": total_value,
        })
    finally:
        db.close()

@app.post("/inventory/goal", response_class=HTMLResponse)
async def set_goal_html(
    request: Request,
    item_name: str = Form(...),
    goal_quantity: int = Form(...)
):
    db = SessionLocal()
    try:
        item_db = db.query(Item).filter(Item.name.ilike(item_name)).first()

        goal_message = None
        goal_error = None

        if not item_db:
            goal_error = f"Item '{item_name}' não encontrado no catálogo."
        else:
            inv = db.query(UserInventory).filter(
                UserInventory.user_id == USER_ID,
                UserInventory.item_id == item_db.id
            ).first()
            if inv:
                inv.goal_quantity = goal_quantity
            else:
                db.add(UserInventory(
                    user_id=USER_ID,
                    item_id=item_db.id,
                    quantity=0,
                    goal_quantity=goal_quantity
                ))
            db.commit()
            goal_message = f"Meta de {goal_quantity}x {item_db.name} definida com sucesso!"

        entradas = db.query(UserInventory).filter(
            UserInventory.user_id == USER_ID
        ).all()
        resultado = []
        total_value = 0
        for entrada in entradas:
            it = db.query(Item).filter(Item.id == entrada.item_id).first()
            if not it:
                continue
            val = it.npc_price * entrada.quantity
            total_value += val
            resultado.append({
                "item": it.name,
                "quantity": entrada.quantity,
                "goal_quantity": entrada.goal_quantity,
                "goal_reached": entrada.quantity >= entrada.goal_quantity if entrada.goal_quantity > 0 else None,
                "npc_price": it.npc_price,
                "npc_seller": it.npc_seller,
                "is_imbuement_material": it.is_imbuement_material,
                "imbuement_name": it.imbuement_name,
                "estimated_value": val
            })
        resultado.sort(key=lambda x: x["estimated_value"], reverse=True)

        return templates.TemplateResponse("inventory.html", {
            "request": request,
            "active": "inventory",
            "items": resultado,
            "total_value": total_value,
            "goal_message": goal_message,
            "goal_error": goal_error,
        })
    finally:
        db.close()

def _processar_hunt_html(hunt_data, db):
    bestiary_updates = []
    for item_coletado in hunt_data.items:
        item_db = db.query(Item).filter(Item.name.ilike(item_coletado.name)).first()
        if not item_db:
            continue
        inv = db.query(UserInventory).filter(
            UserInventory.user_id == USER_ID,
            UserInventory.item_id == item_db.id
        ).first()
        if inv:
            inv.quantity += item_coletado.quantity
        else:
            db.add(UserInventory(
                user_id=USER_ID,
                item_id=item_db.id,
                quantity=item_coletado.quantity,
                goal_quantity=0
            ))

    for criatura in hunt_data.creatures:
        criatura_db = db.query(Creature).filter(
            Creature.name.ilike(criatura.name)
        ).first()
        if not criatura_db:
            continue
        entrada = db.query(BestiaryEntry).filter(
            BestiaryEntry.user_id == USER_ID,
            BestiaryEntry.creature_id == criatura_db.id
        ).first()
        kills_before = entrada.kills_current if entrada else 0
        kills_after = kills_before + criatura.kills
        completed = kills_after >= criatura_db.kills_required
        if entrada:
            entrada.kills_current = kills_after
            entrada.completed = completed
        else:
            db.add(BestiaryEntry(
                user_id=USER_ID,
                creature_id=criatura_db.id,
                kills_current=kills_after,
                completed=completed
            ))
        bestiary_updates.append({
            "creature": criatura_db.name,
            "kills_before": kills_before,
            "kills_after": kills_after,
            "total_required": criatura_db.kills_required,
            "completed": completed,
            "charm_points_earned": criatura_db.charm_points if completed else None
        })

    db.commit()
    decisoes = gerar_relatorio_venda(hunt_data.items, db, USER_ID)

    inv_all = db.query(UserInventory).filter(UserInventory.user_id == USER_ID).all()
    total_value = sum(
        (db.query(Item).filter(Item.id == e.item_id).first().npc_price or 0) * e.quantity
        for e in inv_all
    )
    progresso = get_progresso_bestiary(db, USER_ID)
    total_pontos = get_total_charm_points(db, USER_ID)

    return {
        "active": "dashboard",
        "total_items": len(inv_all),
        "total_value": total_value,
        "total_creatures": len(progresso),
        "completed_creatures": sum(1 for c in progresso if c["completed"]),
        "total_charm_points": total_pontos,
        "decisoes": decisoes,
        "bestiary_updates": bestiary_updates,
    }