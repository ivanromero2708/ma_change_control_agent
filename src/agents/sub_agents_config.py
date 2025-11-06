from src.prompts.sub_agent_prompts import *
from src.tools import *

legacy_migration_subagent = {
    "name": "legacy_migration_agent",
    "description": "Delega a este agente siempre que te entreguen un documento de método analítico legado. Este agente se encargará de ejecutar las herramientas requeridas para generar un json estructurado con el método analítico en el formato nuevo",
    "system_prompt": LEGACY_MIGRATION_AGENT_INSTRUCTIONS,
    "tools": [extract_legacy_sections, structure_specs_procs, consolidar_pruebas_procesadas],
    "model": "openai:gpt-5-mini"
}