"""Grava cenário real controlado de falha de API para vídeo acadêmico.

O servidor principal em 18501 e API real em 18000 continuam intactos.
Esta instância isolada usa uma API inativa em 18599 para mostrar o fallback.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from scripts.gravar_demo_video import BASE, save, capture_chapter, VIDEO_W, VIDEO_H
URL="http://127.0.0.1:18502"
manifest_file=BASE/"manifest.json"
assert manifest_file.exists(),"Manifesto da gravação inicial ausente."
manifest=json.loads(manifest_file.read_text(encoding="utf-8"))
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    ctx=browser.new_context(
        viewport={"width": VIDEO_W,"height": VIDEO_H},
        record_video_dir=str(BASE),
        record_video_size={"width": VIDEO_W,"height": VIDEO_H},
        color_scheme="light",device_scale_factor=1,
    )
    page=ctx.new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=30000)
    page.get_by_text("Serviço Indisponível",exact=False).first.wait_for(timeout=30000)
    start=time.monotonic();bookmarks=[]
    def show_error():
        page.mouse.move(144,369,steps=15)
        time.sleep(4)
        page.mouse.move(770,412,steps=25)
        time.sleep(3)
        page.mouse.wheel(0,215)
        time.sleep(3)
        page.mouse.move(1010,580,steps=20)
        time.sleep(2)
    capture_chapter(page,bookmarks,"ui_erro",16,show_error)
    manifest["erro"]=save(ctx,page,"erro",bookmarks,start)
    browser.close()
manifest_file.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print("MANIFEST_OK",manifest_file,flush=True)
