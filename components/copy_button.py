import streamlit.components.v1 as components, html, random

# パスワード＋コピー機能をセットで表示
def copy_button_row(text, label="コピー"):
    esc = html.escape(text, quote=True)
    bid = f"btn_{random.randrange(1_000_000)}"
    components.html(
        f"""<div style="display:flex;align-items:center;margin-bottom:8px;">
               <code style="flex:1;font-size:16px;">{esc}</code>
               <button id="{bid}" style="margin-left:10px;">{label}</button>
           </div>
           <script>
             const b=document.getElementById("{bid}");
             b.onclick=()=>{{
               navigator.clipboard.writeText("{text}");
               b.textContent="コピー済み";
               setTimeout(()=>b.textContent="{label}",1000);
             }};
           </script>
        """, height=50)
