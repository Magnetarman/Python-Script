#!/usr/bin/env python33
# Esporta la "fotografia" completa e interattiva di una struttura di cartelle in un file HTML statico

from __future__ import annotations


import os
import sys
import traceback
import subprocess
import getpass
from datetime import datetime, date
from typing import Optional, Tuple, List


# Proviamo a usare anytree, se non disponibile fallback a treelib
USING_ANYTREE = False
USING_TREELIB = False

try:
    from anytree import Node, PreOrderIter
    USING_ANYTREE = True
except Exception:
    try:
        from treelib import Node as TLNode, Tree as TLTree
        USING_TREELIB = True
    except Exception:
        print(
            "Errore: è richiesta la libreria 'anytree' o, in alternativa, 'treelib'.\n"
            "Installa con: pip install anytree   (oppure)   pip install treelib",
            file=sys.stderr,
        )
        sys.exit(1)


# ------------------------- Utility di formattazione ------------------------- #

def sizeof_fmt(num: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if num < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} EB"


def get_creation_time(path: str) -> float:
    try:
        stat = os.stat(path)
        if hasattr(stat, "st_birthtime") and stat.st_birthtime:
            return stat.st_birthtime
        return stat.st_ctime if os.name == "nt" else stat.st_mtime
    except Exception:
        try:
            return os.path.getmtime(path)
        except Exception:
            return 0.0


def fmt_datetime(ts: float) -> str:
    if not ts:
        return "-"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


# ------------------------------ Scansione FS ------------------------------- #

class FSNodeData:
    __slots__ = ("name", "full_path", "is_dir", "ctime", "size_bytes")

    def __init__(self, name: str, full_path: str, is_dir: bool, ctime: float, size_bytes: int = 0):
        self.name = name
        self.full_path = full_path
        self.is_dir = is_dir
        self.ctime = ctime
        self.size_bytes = size_bytes


def scan_directory(root_path: str):
    """Crea l'albero dei nodi a partire da root_path e calcola le dimensioni cumulative.

    Ritorna una tupla: (root_node, total_nodes, skipped_items, errors)
    La struttura del nodo dipende dalla libreria disponibile (anytree o treelib).
    """
    root_path = os.path.abspath(root_path)
    root_data = FSNodeData(
        name=os.path.basename(root_path) or root_path,
        full_path=root_path,
        is_dir=True,
        ctime=get_creation_time(root_path),
        size_bytes=0,
    )

    errors: List[str] = []
    skipped = 0
    total_nodes = 1

    if USING_ANYTREE:
        root_node = Node(root_data.name, data=root_data)

        def _walk(parent_node: Node):
            nonlocal skipped, total_nodes
            try:
                with os.scandir(parent_node.data.full_path) as it:
                    for entry in it:
                        try:
                            is_dir = entry.is_dir(follow_symlinks=False)
                            data = FSNodeData(
                                name=entry.name,
                                full_path=entry.path,
                                is_dir=is_dir,
                                ctime=get_creation_time(entry.path),
                                size_bytes=0,
                            )
                            child = Node(data.name, parent=parent_node, data=data)
                            total_nodes += 1
                            if is_dir:
                                _walk(child)
                            else:
                                try:
                                    data.size_bytes = entry.stat(follow_symlinks=False).st_size
                                except Exception:
                                    skipped += 1
                        except PermissionError:
                            skipped += 1
                        except Exception:
                            skipped += 1
                            errors.append(traceback.format_exc(limit=1))
            except PermissionError:
                skipped += 1
            except Exception:
                skipped += 1
                errors.append(traceback.format_exc(limit=1))

        _walk(root_node)

        # Calcolo dimensioni cumulative per le cartelle (bottom-up)
        for node in reversed(list(PreOrderIter(root_node))):
            if node.data.is_dir:
                # somma delle dimensioni dei figli
                node.data.size_bytes = sum((c.data.size_bytes for c in node.children), 0)
        return root_node, total_nodes, skipped, errors

    elif USING_TREELIB:
        tree = TLTree()
        root_node = TLNode(identifier=root_data.full_path, tag=root_data.name, data=root_data)
        tree.add_node(root_node)

        def _walk(parent: TLNode):
            nonlocal skipped, total_nodes
            try:
                with os.scandir(parent.data.full_path) as it:
                    for entry in it:
                        try:
                            is_dir = entry.is_dir(follow_symlinks=False)
                            data = FSNodeData(
                                name=entry.name,
                                full_path=entry.path,
                                is_dir=is_dir,
                                ctime=get_creation_time(entry.path),
                                size_bytes=0,
                            )
                            child = TLNode(identifier=data.full_path, tag=data.name, data=data)
                            tree.add_node(child, parent=parent)
                            total_nodes += 1
                            if is_dir:
                                _walk(child)
                            else:
                                try:
                                    data.size_bytes = entry.stat(follow_symlinks=False).st_size
                                except Exception:
                                    skipped += 1
                        except PermissionError:
                            skipped += 1
                        except Exception:
                            skipped += 1
                            errors.append(traceback.format_exc(limit=1))
            except PermissionError:
                skipped += 1
            except Exception:
                skipped += 1
                errors.append(traceback.format_exc(limit=1))

        _walk(root_node)

        # bottom-up: calcola le dimensioni cartelle
        for node in reversed(tree.all_nodes()):
            if node.data.is_dir:
                node.data.size_bytes = sum((tree[node_id].data.size_bytes for node_id in tree.is_branch(node.identifier)), 0)
        return tree, total_nodes, skipped, errors

    else:  # Non dovrebbe accadere
        raise RuntimeError("Nessuna libreria di albero disponibile.")


# ------------------------------ HTML Rendering ----------------------------- #

INLINE_CSS = r"""
:root { --font: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Noto Sans', 'Helvetica Neue', Arial, 'Apple Color Emoji', 'Segoe UI Emoji'; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; font-family: var(--font); }
header { padding: 16px; background: #f0f0f0; border-bottom: 1px solid #e0e0e0; }
main { padding: 16px; }
.summary { font-size: 14px; color: #333; margin-top: 4px; }
.controls { display: flex; gap: 8px; flex-wrap: wrap; margin: 12px 0; }
button { border: 1px solid #ccc; padding: 8px 12px; border-radius: 8px; cursor: pointer; background: white; }
button:hover { background: #f9f9f9; }
.tree { list-style: none; padding-left: 0; }
.tree ul { list-style: none; margin: 0; padding-left: 20px; }
.tree li { margin: 2px 0; }
.node { display: grid; grid-template-columns: auto 1fr auto auto; gap: 8px; align-items: center; }
.icon { width: 16px; height: 16px; display: inline-block; }
.name { font-weight: 500; word-break: break-word; }
.meta { font-size: 12px; color: #555; }
.size { font-variant-numeric: tabular-nums; font-size: 12px; color: #333; }
.ctime { font-size: 12px; color: #666; }
.folder > .node { cursor: pointer; }
.hidden { display: none; }
.footer { margin-top: 24px; font-size: 12px; color: #666; }
@media (max-width: 640px) { .node { grid-template-columns: auto 1fr; } .size, .ctime { grid-column: 2; } }
"""

INLINE_JS = r"""
function toggle(el) {
  const children = el.parentElement.querySelector(':scope > ul');
  if (children) { children.classList.toggle('hidden'); }
}
function expandAll() {
  document.querySelectorAll('.tree ul').forEach(ul => ul.classList.remove('hidden'));
}
function collapseAll() {
  document.querySelectorAll('.tree ul').forEach(ul => ul.classList.add('hidden'));
}
function filterTree() {
    const q = document.getElementById('q').value.toLowerCase();
    const items = document.querySelectorAll('.tree li');
    items.forEach(function(item) {
        const nameSpan = item.querySelector('.name');
        const name = nameSpan ? nameSpan.textContent.toLowerCase() : '';
        let match = q === '' || (name && name.includes(q));
        if (!match) {
            // Se non corrisponde, controllo se uno dei figli visibili corrisponde
            const childMatch = Array.from(item.querySelectorAll(':scope > ul > li')).some(
                child => child.style.display !== 'none'
            );
            match = childMatch;
        }
        item.style.display = match ? '' : 'none';
    });
}
"""

# Icone SVG inline (cartella/file)
FOLDER_SVG = """<svg class=\"icon\" viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M10 4l2 2h8a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2h6z\"></path></svg>"""
FILE_SVG = """<svg class=\"icon\" viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6\"></path></svg>"""


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
         .replace("'", "&#039;")
    )


def render_node_anytree(node) -> str:
    d: FSNodeData = node.data
    name = html_escape(d.name)
    size = html_escape(sizeof_fmt(d.size_bytes))
    ctime = html_escape(fmt_datetime(d.ctime))

    if d.is_dir:
        # Cartella con figli
        children_html = "\n".join(render_node_anytree(c) for c in node.children)
        return (
            f"<li class='folder' data-name='{name}'>"
            f"<div class='node' onclick='toggle(this)'>{FOLDER_SVG}<div class='name'>{name}</div>"
            f"<div class='size'>{size}</div><div class='ctime'>{ctime}</div></div>"
            f"<ul class=''>\n{children_html}\n</ul>"
            f"</li>"
        )
    else:
        # File
        return (
            f"<li class='file' data-name='{name}'>"
            f"<div class='node'>{FILE_SVG}<div class='name'>{name}</div>"
            f"<div class='size'>{size}</div><div class='ctime'>{ctime}</div></div>"
            f"</li>"
        )


def render_node_treelib(tree: 'TLTree', node: 'TLNode') -> str:
    d: FSNodeData = node.data
    name = html_escape(d.name)
    size = html_escape(sizeof_fmt(d.size_bytes))
    ctime = html_escape(fmt_datetime(d.ctime))

    children = tree.children(node.identifier)
    if d.is_dir:
        children_html = "\n".join(render_node_treelib(tree, ch) for ch in children)
        return (
            f"<li class='folder' data-name='{name}'>"
            f"<div class='node' onclick='toggle(this)'>{FOLDER_SVG}<div class='name'>{name}</div>"
            f"<div class='size'>{size}</div><div class='ctime'>{ctime}</div></div>"
            f"<ul class=''>\n{children_html}\n</ul>"
            f"</li>"
        )
    else:
        return (
            f"<li class='file' data-name='{name}'>"
            f"<div class='node'>{FILE_SVG}<div class='name'>{name}</div>"
            f"<div class='size'>{size}</div><div class='ctime'>{ctime}</div></div>"
            f"</li>"
        )


def render_html(root_obj, root_path: str, total_nodes: int, skipped: int) -> str:
    today = date.today().isoformat()
    root_name = os.path.basename(root_path) or root_path
    root_name_html = html_escape(root_name)

    if USING_ANYTREE:
        body_tree = render_node_anytree(root_obj)
    else:
        # treelib
        body_tree = render_node_treelib(root_obj, root_obj.get_node(root_obj.root)) if hasattr(root_obj, 'get_node') else render_node_treelib(root_obj, root_obj)

    html = f"""
<!DOCTYPE html>
<html lang=\"it\">
<head>
<meta charset=\"utf-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
<title>Export struttura - {root_name_html}</title>
<style>{INLINE_CSS}</style>
</head>
<body>
<header>
  <h1>Esportazione struttura: {root_name_html}</h1>
  <div class=\"summary\">Creato il {today} • Nodi totali: {total_nodes} • Elementi non accessibili: {skipped}</div>
  <div class=\"controls\">
    <input id=\"q\" type=\"search\" placeholder=\"Filtra per nome...\" oninput=\"filterTree()\" style=\"flex:1; min-width: 180px; padding:8px; border:1px solid #ccc; border-radius:8px;\" />
    <button onclick=\"expandAll()\">Espandi tutto</button>
    <button onclick=\"collapseAll()\">Comprimi tutto</button>
  </div>
</header>
<main>
  <ul class=\"tree\">{body_tree}</ul>
  <div class=\"footer\">Questo file è stato generato come istantanea statica: non contiene collegamenti al percorso originale.</div>
</main>
<script>{INLINE_JS}</script>
</body>
</html>
"""
    return html


# ------------------------------- Validazione ------------------------------- #

def try_mount_unc(path: str) -> None:
    """Se il percorso è UNC e non accessibile, chiede credenziali e prova a montarlo con net use."""
    if os.name != "nt":
        return  # solo Windows

    if not (path.startswith("\\\\") or path.startswith("//")):
        return

    # Percorso UNC non accessibile → chiediamo credenziali
    print(f"Il percorso {path} non è accessibile. Inserisci credenziali per la condivisione.")
    user = input("Utente (DOMINIO\\utente o utente): ").strip()
    pwd = getpass.getpass("Password: ")

    try:
        cmd = ["net", "use", path, pwd, f"/user:{user}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Errore nel montaggio con net use:", result.stderr, file=sys.stderr)
        else:
            print("Condivisione montata con successo.")
    except Exception as e:
        print(f"Errore nell'esecuzione di net use: {e}", file=sys.stderr)


def validate_path(p: str) -> str:
    p = p.strip().strip('"').strip("'")
    if not p:
        raise ValueError("Percorso vuoto.")
    p = os.path.expanduser(p)
    abs_p = os.path.abspath(p)

    if not os.path.exists(abs_p):
        try_mount_unc(p)

    if not os.path.exists(abs_p):
        raise FileNotFoundError(f"Il percorso non esiste o non è accessibile: {abs_p}")

    if not os.path.isdir(abs_p):
        raise NotADirectoryError(f"Il percorso deve essere una cartella: {abs_p}")

    if not os.access(abs_p, os.R_OK):
        raise PermissionError(f"Permesso negato per la lettura: {abs_p}")

    return abs_p


# --------------------------------- Main ----------------------------------- #

def main():
    print("Inserisci un percorso da analizzare (es. C:\\cartella oppure \\\\server\\share):")
    user_input = input("> ").strip()
    try:
        root_path = validate_path(user_input)
    except Exception as e:
        print(f"Errore di validazione: {e}", file=sys.stderr)
        sys.exit(2)

    print("Scansione in corso... Questa operazione può richiedere tempo per strutture molto grandi.")
    root_obj, total_nodes, skipped, errors = scan_directory(root_path)

    if errors:
        print(f"Avvisi/Errori durante la scansione: {len(errors)}", file=sys.stderr)

    print("Generazione HTML...")
    html = render_html(root_obj, root_path, total_nodes, skipped)

    now = datetime.now()
    out_name = f"Export_data_{now.strftime('%Y-%m-%d_%H-%M-%S')}.html"
    with open(out_name, "w", encoding="utf-8", newline="") as f:
        f.write(html)

    print(f"Fatto. File generato: {out_name}")


if __name__ == "__main__":
    try:
        while True:
            main()
            scelta = input("\nUtilizza di nuovo lo script digitando 1 o premi 0 per ritornare a main.py: ").strip()
            if scelta == '1':
                continue
            elif scelta == '0':
                break
            else:
                print("Scelta non valida. Inserire 1 o 0.")
    except KeyboardInterrupt:
        print("Interrotto dall'utente.")
